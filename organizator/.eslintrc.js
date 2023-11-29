module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    jest: true,
    node: true,
  },
  extends: ["universe/native"],
  plugins: ["prettier"],
  ignorePatterns: [
    "*.svg",
    "*.css",
    "*.scss",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.json",
    "*.md",
    "*.ico",
  ],
};
