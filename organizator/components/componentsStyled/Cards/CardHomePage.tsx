import React from "react";
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
  isStudent?: boolean;
}

export default function CardHomePage(props: CardProps) {
  const { title, startDate, endDate, location, headerImage, isStudent } = props;

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
      </CardTextContainer>
      {isStudent && (
        <AbsoluteChip name="Students only" backgroundColor="#b3f3f5" />
      )}
    </CardContainer>
  );
}
