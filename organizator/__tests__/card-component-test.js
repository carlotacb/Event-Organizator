import * as React from "react";
// eslint-disable-next-line import/no-extraneous-dependencies
import renderer from "react-test-renderer";
import CardHomePage from "../components/componentsStyled/Cards/CardHomePage";

it(`renders correctly a button`, () => {
  const tree = renderer
    .create(
      <CardHomePage
        title="Test event"
        startDate="2023-12-2200:36:41.562401TZ"
        endDate="2023-12-2117:27:38.081421TZ"
        location="UPC campus nord"
        id="this-is-a-test-id"
        headerImage="https://media.istockphoto.com/id/1087531642/vector/male-face-silhouette-or-icon-man-avatar-profile-unknown-or-anonymous-person-vector.jpg?s=612x612&w=0&k=20&c=FEppaMMfyIYV2HJ6Ty8tLmPL1GX6Tz9u9Y8SCRrkD-o%3D"
      />,
    )
    .toJSON();

  expect(tree).toMatchSnapshot();
});
