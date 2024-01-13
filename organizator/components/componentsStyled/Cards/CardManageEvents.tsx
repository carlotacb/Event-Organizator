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
          <CardText color="black">
            Registered: {participants} participants
          </CardText>
        </TextLine>
        <TextLine>
          <CardText color="black">
            Remaining: {spots - participants} spots
          </CardText>
        </TextLine>
        <TextLine>
          <Progress.Bar
            progress={progress}
            height={15}
            color={progress > expectedAttrition ? "green" : "lightcoral"}
          />
          <CardText color="black">{progressPercentage} %</CardText>
        </TextLine>

        <CardSubtitle color="#233B77">Expected</CardSubtitle>
        <TextLine>
          <CardText color="dimgray">{maxParticipants} participants</CardText>
        </TextLine>
        <TextLine>
          <CardText color="dimgray">
            {expectedAttrition * 100}% attrition rate
          </CardText>
        </TextLine>
        <TextLine>
          <CardText color="dimgray">
            {spots} participants available spots
          </CardText>
        </TextLine>
      </CardTextContainer>
    </CardContainer>
  );
}
