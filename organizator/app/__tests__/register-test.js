import * as React from "react";
// eslint-disable-next-line import/no-extraneous-dependencies
import renderer from "react-test-renderer";
import RegisterPage from "../register";

it(`renders correctly`, () => {
  const tree = renderer.create(<RegisterPage />).toJSON();

  expect(tree).toMatchSnapshot();
});
