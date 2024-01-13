import * as React from "react";
// eslint-disable-next-line import/no-extraneous-dependencies
import renderer from "react-test-renderer";
import Input from "../components/componentsStyled/Forms/Input";

it(`renders correctly a input with only label`, () => {
  const tree = renderer.create(<Input label="username" />).toJSON();

  expect(tree).toMatchSnapshot();
});

it(`renders correctly a input with label and value`, () => {
  const tree = renderer
    .create(<Input label="username" value="test" />)
    .toJSON();

  expect(tree).toMatchSnapshot();
});

it(`renders correctly a input with label and value and error`, () => {
  const tree = renderer
    .create(<Input label="username" value="test" error="error" />)
    .toJSON();

  expect(tree).toMatchSnapshot();
});

it(`renders correctly a input with label and value that is password`, () => {
  const tree = renderer
    .create(<Input label="password" value="test" password />)
    .toJSON();

  expect(tree).toMatchSnapshot();
});

it(`renders correctly a input with label and value that is required`, () => {
  const tree = renderer
    .create(<Input label="username" value="test" required />)
    .toJSON();

  expect(tree).toMatchSnapshot();
});

it(`renders correctly a input with label and value that is disabled`, () => {
  const tree = renderer
    .create(<Input label="username" value="test" disabled />)
    .toJSON();

  expect(tree).toMatchSnapshot();
});

it(`renders correctly a input with value and icon`, () => {
  const tree = renderer
    .create(<Input label="username" value="test" icon="user" />)
    .toJSON();

  expect(tree).toMatchSnapshot();
});
