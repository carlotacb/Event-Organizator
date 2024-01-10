import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import * as Progress from "react-native-progress";

interface CardProps {
  title: string;
  participants: number;
  maxParticipants: number;
  expectedAttrition: number;
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

const CardTextContainer = styled.View`
  padding: 25px;
`;

const CardTitle = styled.Text`
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
`;

const CardSubtitle = styled.Text<{ color: string }>`
  font-size: 18px;
  font-weight: bold;
  margin-top: 15px;
  color: ${(props: { color: string }) => props.color};
`;

const CardText = styled.Text<{ color: string }>`
  font-size: 16px;
  color: ${(props: { color: string }) => props.color};
`;

const TextLine = styled.View`
  display: flex;
  flex-direction: row;
  gap: 10px;
  margin-top: 10px;
`;

const TextLineRow = styled.View`
  display: flex;
  flex-direction: row;
  gap: 10px;
  margin-top: 10px;
  align-items: center;
`;

export default function CardManageEvents(props: CardProps) {
  const { title, participants, maxParticipants, expectedAttrition } = props;

  const spots = expectedAttrition * maxParticipants + maxParticipants;
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
        <TextLineRow>
          <Progress.Bar progress={progress} height={15} color="green" />
          <CardText>{progressPercentage} %</CardText>
        </TextLineRow>

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
          <CardText color="dimgray">{spots} participants to register</CardText>
        </TextLine>
      </CardTextContainer>
    </CardContainer>
  );
}
