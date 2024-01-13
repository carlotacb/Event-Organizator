import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import { FontAwesome5 } from "@expo/vector-icons";
import { parseDate } from "../../../utils/util-functions";
import {
  CardContainer,
  CardImage,
  CardText,
  CardTextContainer,
  CardTitle,
  TextLine,
} from "./Styles";
import AbsoluteChip from "../Chips/AbsoluteChip";

interface CardProps {
  // eslint-disable-next-line react/no-unused-prop-types
  id: string;
  title: string;
  startDate: string;
  endDate: string;
  location: string;
  headerImage: string;
  students: boolean;
}

const PastTag = styled.View`
  position: absolute;
  top: 25px;
  right: 25px;
  border: 4px solid #772323;
  background-color: rgba(119, 35, 35, 0.8);
  border-radius: 20px;
  padding: 5px 15px;
`;

const PastText = styled.Text`
  color: white;
  font-weight: bold;
  font-size: 20px;
`;

export default function CardHomePage(props: CardProps) {
  const { title, startDate, endDate, location, headerImage, students } = props;

  const isPast = () => startDate < new Date().toISOString();

  return (
    <CardContainer isPast={isPast()}>
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
        {isPast() && (
          <PastTag>
            <PastText>Past</PastText>
          </PastTag>
        )}
      </CardTextContainer>
      {students && (
        <AbsoluteChip name="Students only" backgroundColor="#b3f3f5" />
      )}
    </CardContainer>
  );
}
