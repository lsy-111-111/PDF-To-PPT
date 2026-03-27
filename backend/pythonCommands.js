function isTruthyFlag(value) {
  return value === true || value === "true";
}

function buildEditorCommandArgs({ dirName, downloadImages, useSam2 = false }) {
  const args = ["editortry.py", dirName, String(downloadImages)];

  if (useSam2) {
    args.push("--use-sam2");
  }

  return args;
}

function buildCnnConvertArgs({ dirName, downloadImages }) {
  return ["cnn_convertor.py", dirName, String(downloadImages)];
}

module.exports = {
  buildCnnConvertArgs,
  buildEditorCommandArgs,
  isTruthyFlag,
};
