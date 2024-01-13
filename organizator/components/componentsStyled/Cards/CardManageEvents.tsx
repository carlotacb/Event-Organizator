import React from "react";
import * as Progress from "react-native-progress";
import {
  CardContainer,
  CardSubtitle,
  CardText,
  CardTextContainer,
  CardTitle,
  TextLine,
} from "./Styles";
import { systemColors } from "../tokens";

interface CardProps {
  title: string;
  participants: number;
  maxParticipants: number;
  expectedAttrition: number;
}

export default function CardManageEvents(props: CardProps) {
  const { title, participants, maxParticipants, expectedAttrition } = props;

  const spots =
    Math.ceil(expectedAttrition * maxParticipants) + maxParticipants;
  const progress = participants / spots;
  const progressPercentage = (progress * 100).toFixed(2);

  return (
    <CardContainer>
      <CardTextContainer>
        <CardTitle>{title}</CardTitle>
        <TextLine>
          <CardText>Registered: {participants} participants</CardText>
        </TextLine>
        <TextLine>
          <CardText>Remaining: {spots - participants} spots</CardText>
        </TextLine>
        <TextLine>
          <Progress.Bar
            progress={progress}
            height={15}
            color={progress > expectedAttrition ? "green" : "lightcoral"}
          />
          <CardText>{progressPercentage} %</CardText>
        </TextLine>

        <CardSubtitle color={systemColors.subtitleColor}>Expected</CardSubtitle>
        <TextLine>
          <CardText color={systemColors.subtitleColor}>
            {maxParticipants} participants
          </CardText>
        </TextLine>
        <TextLine>
          <CardText color={systemColors.subtitleColor}>
            {expectedAttrition * 100}% attrition rate
          </CardText>
        </TextLine>
        <TextLine>
          <CardText color={systemColors.subtitleColor}>
            {spots} participants available spots
          </CardText>
        </TextLine>
      </CardTextContainer>
    </CardContainer>
  );
}
