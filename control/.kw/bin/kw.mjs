#!/usr/bin/env node
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const RUNTIME_PACKAGE = "@knowledge-workshop/runtime";
const currentFile = fileURLToPath(import.meta.url);
const consumerRoot = path.resolve(path.dirname(currentFile), "..", "..");
const lockPath = path.join(consumerRoot, ".kw", "kw-lock.json");

function fail(message) {
  console.error(message);
  process.exit(1);
}

function readJson(filePath) {
  return JSON.parse(readFileSync(filePath, "utf8"));
}

function readJsonIfExists(filePath) {
  return existsSync(filePath) ? readJson(filePath) : null;
}

function exactVersion(value) {
  return /^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/.test(value);
}

function readLockVersion() {
  if (!existsSync(lockPath)) {
    fail(`Missing Knowledge Workshop lock: ${lockPath}`);
  }
  const payload = readJson(lockPath);
  const version = payload && payload.workshop && payload.workshop.version;
  if (!version) {
    fail(`Knowledge Workshop lock is missing workshop.version: ${lockPath}`);
  }
  const normalized = String(version);
  if (!exactVersion(normalized)) {
    fail(`Knowledge Workshop lock must contain an exact runtime version, got: ${normalized}`);
  }
  return normalized;
}

function cliPath(runtimeRoot) {
  return path.join(runtimeRoot, "dist", "kw", "cli.js");
}

function packageNodeModulesPath(root, name) {
  return name.startsWith("@")
    ? path.join(root, "node_modules", ...name.split("/"))
    : path.join(root, "node_modules", name);
}

function npmRunner(env = process.env) {
  const npmExecPath = env.npm_execpath || "";
  if (npmExecPath) {
    const extension = path.extname(npmExecPath).toLowerCase();
    if ([".js", ".cjs", ".mjs"].includes(extension)) {
      return { command: process.execPath, args: [npmExecPath] };
    }
    if (process.platform === "win32") {
      return { command: env.ComSpec || "cmd.exe", args: ["/d", "/c", npmExecPath] };
    }
    return { command: npmExecPath, args: [] };
  }
  if (process.platform === "win32") {
    return { command: process.env.ComSpec || "cmd.exe", args: ["/d", "/c", "npm"] };
  }
  return { command: "npm", args: [] };
}

function runNpm(args, cwd, options = {}) {
  const runner = npmRunner(options.env || process.env);
  const result = spawnSync(runner.command, [...runner.args, ...args], {
    cwd,
    env: options.env || process.env,
    encoding: "utf8",
    stdio: "pipe"
  });
  if (result.error) {
    fail(`npm failed: ${result.error.message}`);
  }
  if (result.status !== 0) {
    fail((result.stderr || result.stdout || "").trim() || `npm failed with exit code ${result.status}`);
  }
}

function withProjectedNpmrc(projectRoot, npmRoot, action) {
  const source = path.join(projectRoot, ".npmrc");
  const target = path.join(npmRoot, ".npmrc");
  if (!existsSync(source) || path.resolve(source) === path.resolve(target)) {
    return action();
  }
  const hadTarget = existsSync(target);
  const previous = hadTarget ? readFileSync(target) : Buffer.alloc(0);
  const sourceContent = readFileSync(source);
  try {
    mkdirSync(npmRoot, { recursive: true });
    writeFileSync(target, hadTarget ? Buffer.concat([previous, Buffer.from("\n"), sourceContent]) : sourceContent);
    return action();
  } finally {
    if (hadTarget) {
      writeFileSync(target, previous);
    } else {
      rmSync(target, { force: true });
    }
  }
}

function sha256(filePath) {
  return createHash("sha256").update(readFileSync(filePath)).digest("hex");
}

function isPathInside(parent, target) {
  const relative = path.relative(path.resolve(parent), path.resolve(target));
  return relative === "" || (!!relative && !relative.startsWith("..") && !path.isAbsolute(relative));
}

function runtimePayloadRoot(packageRoot) {
  const manifestPath = path.join(packageRoot, "knowledge-workshop-runtime.json");
  if (!existsSync(manifestPath)) {
    fail(`runtime package is missing knowledge-workshop-runtime.json: ${packageRoot}`);
  }
  const manifest = readJson(manifestPath);
  const payloadRoot = path.resolve(packageRoot, String(manifest.payload_root || "payload"));
  if (!isPathInside(packageRoot, payloadRoot) || !existsSync(cliPath(payloadRoot))) {
    fail(`runtime package payload is incomplete: ${packageRoot}`);
  }
  return payloadRoot;
}

function verifyChecksums(packageRoot, payloadRoot) {
  const checksumsPath = path.join(packageRoot, "checksums.json");
  if (!existsSync(checksumsPath)) {
    fail(`runtime package is missing checksums.json: ${packageRoot}`);
  }
  const files = readJson(checksumsPath).files || {};
  for (const [relativePath, expected] of Object.entries(files)) {
    const filePath = path.resolve(payloadRoot, relativePath);
    if (!isPathInside(payloadRoot, filePath) || filePath === payloadRoot || !existsSync(filePath)) {
      fail(`runtime checksum points to an invalid file: ${relativePath}`);
    }
    if (sha256(filePath) !== String(expected)) {
      fail(`runtime checksum mismatch: ${relativePath}`);
    }
  }
}

function ensureRuntimeDependencies(runtimeRoot) {
  const manifest = readJsonIfExists(path.join(runtimeRoot, "package.json"));
  const dependencies = manifest && manifest.dependencies && typeof manifest.dependencies === "object"
    ? Object.keys(manifest.dependencies)
    : [];
  const missing = dependencies.filter((name) => !existsSync(packageNodeModulesPath(runtimeRoot, name)));
  if (missing.length === 0) {
    return;
  }
  withProjectedNpmrc(consumerRoot, runtimeRoot, () => {
    runNpm(["install", "--omit=dev", "--ignore-scripts", "--no-audit", "--no-fund"], runtimeRoot);
  });
}

function installStage(target) {
  mkdirSync(path.dirname(target), { recursive: true });
  return mkdtempSync(path.join(path.dirname(target), ".installing-"));
}

function replaceTarget(stage, target) {
  if (!existsSync(target)) {
    renameSync(stage, target);
    return;
  }
  const backup = `${target}.backup-${process.pid}-${Date.now()}`;
  renameSync(target, backup);
  try {
    renameSync(stage, target);
    rmSync(backup, { recursive: true, force: true });
  } catch (error) {
    rmSync(target, { recursive: true, force: true });
    if (existsSync(backup)) {
      renameSync(backup, target);
    }
    throw error;
  }
}

function installLockedRuntime(version, target) {
  if (process.env.KW_BOOTSTRAP_NO_INSTALL === "1") {
    fail(`Knowledge Workshop runtime ${version} is missing and KW_BOOTSTRAP_NO_INSTALL=1 disables automatic install.`);
  }
  const tempRoot = mkdtempSync(path.join(os.tmpdir(), "kw-runtime-bootstrap-"));
  const stage = installStage(target);
  try {
    runNpm(["install", `${RUNTIME_PACKAGE}@${version}`, "--ignore-scripts", "--no-audit", "--fund=false", "--package-lock=false", "--prefix", tempRoot], consumerRoot);
    const packageRoot = packageNodeModulesPath(tempRoot, RUNTIME_PACKAGE);
    const payloadRoot = runtimePayloadRoot(packageRoot);
    verifyChecksums(packageRoot, payloadRoot);
    // fs.cpSync preserves the package payload shape while keeping install atomic through the staging directory.
    cpSync(payloadRoot, stage, { recursive: true });
    ensureRuntimeDependencies(stage);
    if (!existsSync(cliPath(stage))) {
      fail(`installed runtime is missing dist/kw/cli.js: ${stage}`);
    }
    replaceTarget(stage, target);
  } finally {
    rmSync(tempRoot, { recursive: true, force: true });
    rmSync(stage, { recursive: true, force: true });
  }
}

function resolveRuntimeRoot(version) {
  if (process.env.KW_ROOT) {
    const override = path.resolve(process.env.KW_ROOT);
    if (existsSync(cliPath(override))) {
      return override;
    }
    fail(`KW_ROOT is set but does not contain dist/kw/cli.js: ${override}`);
  }
  const installed = path.join(consumerRoot, ".kw", "local", "versions", version);
  if (!existsSync(cliPath(installed))) {
    installLockedRuntime(version, installed);
  }
  if (existsSync(cliPath(installed))) {
    return installed;
  }
  fail(`Knowledge Workshop runtime ${version} is not installed under ${installed}.`);
}

const version = readLockVersion();
const runtimeRoot = resolveRuntimeRoot(version);
const cli = cliPath(runtimeRoot);
const result = spawnSync(process.execPath, [cli, ...process.argv.slice(2)], {
  cwd: process.cwd(),
  env: { ...process.env, KW_CONSUMER_ROOT: consumerRoot },
  stdio: "inherit"
});

if (result.error) {
  fail(result.error.message);
}
process.exit(result.status ?? 1);
