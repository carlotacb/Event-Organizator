import { Text, View } from "react-native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import React from "react";
import { Link } from "expo-router";
// @ts-ignore
import styled from "styled-components/native";
import { EventInformation } from "../../utils/interfaces/Events";
import {
  Description,
  FirstHeader,
  SubTitleBasic,
  TextLinePlain,
  TextLineText,
  Title,
} from "./Shared/TextStyles";
import { parseDate } from "../../utils/util-functions";

interface EventDetailsProps {
  event: EventInformation | null;
}

const InformationContainer = styled.View`
  padding: 0 20px;
`;

const BasicInfoContainer = styled.View`
  margin-top: 30px;
  background-color: rgba(164, 164, 164, 0.38);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const RestrictionContainer = styled.View`
  margin-top: 30px;
  background-color: rgba(138, 159, 243, 0.2);
  border: 2px solid rgb(138, 159, 243);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const StyledLink = styled(Link)`
  color: blue;
  font-weight: bold;
  font-size: 18px;
`;

export default function EventDetails(props: EventDetailsProps) {
  const { event } = props;

  return (
    <InformationContainer>
      <Title>{event?.name}</Title>
      <Description>{event?.description}</Description>

      <FirstHeader> The information you need to know</FirstHeader>

      <TextLinePlain>
        <FontAwesome name="hourglass-start" />
        <TextLineText>
          Starts the {parseDate(event?.startDate || "")}
        </TextLineText>
      </TextLinePlain>

      <TextLinePlain>
        <FontAwesome name="hourglass-end" />
        <TextLineText>Ends the {parseDate(event?.endDate || "")}</TextLineText>
      </TextLinePlain>

      <TextLinePlain>
        <FontAwesome name="map-marker" />
        <TextLineText>Go to {event?.location}</TextLineText>
      </TextLinePlain>

      <TextLinePlain>
        <FontAwesome name="link" />
        <View
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
          }}
        >
          <TextLineText>Complete information: </TextLineText>
          <StyledLink href={event?.url || ""}>here</StyledLink>
        </View>
      </TextLinePlain>

      <FirstHeader>Restrictions</FirstHeader>

      <TextLinePlain>
        <FontAwesome name="map-marker" />
        <TextLineText>
          You should be at least {event?.minAge} years old
        </TextLineText>
      </TextLinePlain>

      <TextLinePlain>
        <FontAwesome name="map-marker" />
        <TextLineText>
          The event is open for{" "}
          {event?.onlyForStudents ? "only students" : "everyone"}
        </TextLineText>
      </TextLinePlain>
    </InformationContainer>
  );
}
