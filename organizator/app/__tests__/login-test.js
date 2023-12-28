import * as React from "react";
// eslint-disable-next-line import/no-extraneous-dependencies
import renderer from "react-test-renderer";
import LoginPage from "../login";

it(`renders correctly`, () => {
  const tree = renderer.create(<LoginPage />).toJSON();

  expect(tree).toMatchSnapshot();
});
