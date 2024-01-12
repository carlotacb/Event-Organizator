import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import { FontAwesome5 } from "@expo/vector-icons";
import { Text } from "react-native";
import {
  getColorForApplicationStatus,
  parseDate,
} from "../utils/util-functions";

interface CardProps {
  title: string;
  startDate: string;
  headerImage: string;
  status: string;
}

const CardContainer = styled.View<{ isPast: boolean }>`
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
  border-radius: 20px;
  margin: 10px;
  width: 280px;
  opacity: ${(props: { isPast: boolean }) => (props.isPast ? 0.5 : 1)};
`;

const CardImage = styled.Image`
  height: 150px;
  border-radius: 20px;
`;

const CardTextContainer = styled.View`
  padding: 25px 25px 20px;
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
  align-items: center;
  gap: 10px;
  margin-top: 10px;
`;

const PastTag = styled.View`
  position: absolute;
  top: 25px;
  right: 30px;
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

const TagContainer = styled.View`
  display: flex;
  width: 100%;
  margin-top: 20px;
  align-items: flex-end;
`;

const TagStatus = styled.View<{ backgroundColor: string }>`
  border: 2px solid
    ${(props: { backgroundColor: string }) => props.backgroundColor};
  background-color: ${(props: { backgroundColor: string }) =>
    props.backgroundColor};
  padding: 5px 10px;
  border-radius: 20px;
  color: white;
  text-align: center;
`;

export default function CardMyEvents(props: CardProps) {
  const { title, startDate, headerImage, status } = props;

  const isPast = () => startDate < new Date().toISOString();

  return (
    <>
      <CardContainer isPast={isPast()}>
        <CardImage source={{ uri: headerImage }} />
        <CardTextContainer>
          <CardTitle>{title}</CardTitle>
          <TextLine>
            <FontAwesome5 name="calendar" size={16} />
            <CardText>{parseDate(startDate)}</CardText>
          </TextLine>
          <TagContainer>
            <TagStatus backgroundColor={getColorForApplicationStatus(status)}>
              <Text>{status}</Text>
            </TagStatus>
          </TagContainer>
        </CardTextContainer>
      </CardContainer>
      {isPast() && (
        <PastTag>
          <PastText>Past</PastText>
        </PastTag>
      )}
    </>
  );
}
