module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    jest: true,
    node: true,
  },
  extends: [
    "universe/native",
    "airbnb",
    "plugin:react/recommended",
    "plugin:import/typescript",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  plugins: ["@typescript-eslint"],
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
  rules: {
    "prettier/prettier": ["error"],
    "import/extensions": [
      "error",
      "ignorePackages",
      {
        js: "never",
        jsx: "never",
        ts: "never",
        tsx: "never",
      },
    ],
    "react/jsx-filename-extension": [
      2,
      { extensions: [".js", ".jsx", ".ts", ".tsx"] },
    ],
    "react/react-in-jsx-scope": "off",
    "react/require-default-props": "off",
    "react/no-unescaped-entities": "off",
    "no-use-before-define": "off",
    "react/jsx-props-no-spreading": "off",
    "import/no-extraneous-dependencies": [
      "error",
      {
        devDependencies: ["**/*.test.ts", "**/*.test.tsx", "**/*mock-utils.ts"],
      },
    ],
  },
};
