import * as React from "react";
// eslint-disable-next-line import/no-extraneous-dependencies
import renderer from "react-test-renderer";
import Button from "../components/StyledButton";

it(`renders correctly a button`, () => {
  const tree = renderer
    .create(<Button onPress={() => {}} title="Test" />)
    .toJSON();

  expect(tree).toMatchSnapshot();
});
