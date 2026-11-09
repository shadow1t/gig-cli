// Node harness: runs web/templates.js + web/app.js with DOM stubs and tests generate().
// Usage: node tests/test_web.js
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const root = path.join(__dirname, "..");

function makeEl() {
  return {
    addEventListener() {},
    appendChild() {},
    click() {},
    textContent: "",
    innerHTML: "",
    value: "",
    classList: { add() {}, toggle() {}, contains() { return false; } },
  };
}

const elements = {};
const sandbox = {
  document: {
    getElementById: (id) => (elements[id] = elements[id] || makeEl()),
    createElement: () => makeEl(),
    createTextNode: (t) => ({ text: t }),
    body: makeEl(),
  },
  localStorage: { getItem: () => null, setItem() {} },
  history: { replaceState() {} },
  location: { hash: "", pathname: "/" },
  navigator: { clipboard: { writeText: () => Promise.resolve() } },
  URL: { createObjectURL: () => "", revokeObjectURL() {} },
  Blob: function () {},
  setTimeout,
  module: { exports: {} },
};
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(root, "web/templates.js"), "utf8"), sandbox);
vm.runInContext(fs.readFileSync(path.join(root, "web/app.js"), "utf8"), sandbox);

const { generate, resolveName } = sandbox.module.exports;

assert.strictEqual(resolveName("py"), "python");
assert.strictEqual(resolveName("JS"), "node");

const out = generate(["python", "node"]);
assert.ok(out.includes("# ===== python ====="));
assert.ok(out.includes("# ===== node ====="));
assert.ok(out.includes("node_modules/"));
const lines = out.split("\n").map((l) => l.trim());
assert.strictEqual(lines.filter((l) => l === ".env").length, 1, "dedup across templates");

const zig = generate(["zig"]);
assert.ok(zig.includes(".zig-cache/"), "bundled template works");

const count = vm.runInContext("Object.keys(GIG_DATA.templates).length", sandbox);
console.log("web tests: OK (" + count + " templates)");
