import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import { FontAwesome5 } from "@expo/vector-icons";
import { View } from "react-native";
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
  padding: 25px;
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

const Overlay = styled.View`
  flex: 1;
  opacity: 0.5;
  height: 100%;
  width: 100%;
  border-radius: 20px;
`;

const PastTag = styled.View`
  position: absolute;
  top: 15px;
  right: 15px;
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

export default function Card(props: CardProps) {
  const { title, startDate, endDate, location, headerImage } = props;

  const isPast = () => startDate < new Date().toISOString();

  return (
    <CardContainer>
      {isPast() ? (
        <View>
          <Overlay>
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
          </Overlay>
          <PastTag>
            <PastText>Past event</PastText>
          </PastTag>
        </View>
      ) : (
        <>
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
        </>
      )}
    </CardContainer>
  );
}
