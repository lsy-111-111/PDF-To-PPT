const test = require("node:test");
const assert = require("node:assert/strict");

const {
  buildCnnConvertArgs,
  buildEditorCommandArgs,
  isTruthyFlag,
} = require("./pythonCommands");

test("buildEditorCommandArgs keeps legacy arguments when SAM2 is disabled", () => {
  assert.deepEqual(buildEditorCommandArgs({
    dirName: "pdf_123",
    downloadImages: false,
  }), ["editortry.py", "pdf_123", "false"]);
});

test("buildEditorCommandArgs appends the SAM2 flag when enabled", () => {
  assert.deepEqual(buildEditorCommandArgs({
    dirName: "pdf_123",
    downloadImages: true,
    useSam2: true,
  }), ["editortry.py", "pdf_123", "true", "--use-sam2"]);
});

test("buildCnnConvertArgs preserves the existing converter command shape", () => {
  assert.deepEqual(buildCnnConvertArgs({
    dirName: "pdf_123",
    downloadImages: true,
  }), ["cnn_convertor.py", "pdf_123", "true"]);
});

test("isTruthyFlag only accepts boolean true and the true string", () => {
  assert.equal(isTruthyFlag(true), true);
  assert.equal(isTruthyFlag("true"), true);
  assert.equal(isTruthyFlag("false"), false);
  assert.equal(isTruthyFlag(undefined), false);
});
