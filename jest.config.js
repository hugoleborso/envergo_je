module.exports = {
  roots: ["<rootDir>/src"],
  // Jest transformations -- this adds support for TypeScript
  transform: {
    "^.+\\.tsx?$": "ts-jest"
  },
  testEnvironment:"jsdom",

  moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"]
};