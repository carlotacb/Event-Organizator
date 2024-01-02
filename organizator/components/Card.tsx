import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import { FontAwesome5 } from "@expo/vector-icons";
import { parseDate } from "../utils/util-functions";

interface CardProps {
  // eslint-disable-next-line react/no-unused-prop-types
  id: string;
  title: string;
  startDate: string;
  endDate: string;
  location: string;
  headerImage: string;
}

const CardContainer = styled.View`
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
  border-radius: 20px;
  margin: 10px;
  width: 280px;
`;

const CardImage = styled.Image`
  height: 150px;
  border-radius: 20px;
`;

const CardTextContainer = styled.View`
  padding: 20px 25px 30px;
`;

const CardTitle = styled.Text`
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
`;

const CardText = styled.Text`
  font-size: 16px;
`;

const TextLine = styled.View`
  display: flex;
  flex-direction: row;
  gap: 10px;
  margin-top: 10px;
`;

export default function Card(props: CardProps) {
  const { title, startDate, endDate, location, headerImage } = props;

  return (
    <CardContainer>
      <CardImage source={{ uri: headerImage }} />
      <CardTextContainer>
        <CardTitle>{title}</CardTitle>
        <TextLine>
          <FontAwesome5 name="hourglass-start" size={16} />
          <CardText>{parseDate(startDate)}</CardText>
        </TextLine>
        <TextLine>
          <FontAwesome5 name="hourglass-end" size={16} />
          <CardText>{parseDate(endDate)}</CardText>
        </TextLine>
        <TextLine>
          <FontAwesome5 name="map-marker-alt" size={16} />
          <CardText>{location}</CardText>
        </TextLine>
      </CardTextContainer>
    </CardContainer>
  );
}
