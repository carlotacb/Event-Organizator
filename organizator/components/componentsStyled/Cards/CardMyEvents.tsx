import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import { FontAwesome5 } from "@expo/vector-icons";
import { Pressable } from "react-native";
import {
  getColorForApplicationStatus,
  parseDate,
} from "../../../utils/util-functions";
import AbsoluteChip from "../Chips/AbsoluteChip";
import {
  CardContainer,
  CardImage,
  CardText,
  CardTextContainer,
  CardTitle,
  TextLine,
} from "./Styles";

interface CardProps {
  title: string;
  startDate: string;
  headerImage: string;
  status: string;
  id: string;
  setShowCancelAlert: (showCancelAlert: boolean) => void;
  setIdToCancel: (idToCancel: string) => void;
  setShowConfirmAlert: (showConfirmAlert: boolean) => void;
  setIdToConfirm: (idToConfirm: string) => void;
}

const ButtonsContainer = styled.View`
  display: flex;
  flex-direction: column;
  width: 100%;
  justify-content: center;
  align-items: center;
`;

const CancelButton = styled(Pressable)`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 10px;
  margin-top: 15px;
  border-radius: 20px;
  gap: 10px;
  width: 100%;
  background-color: #a65858;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
`;

const ConfirmButton = styled(Pressable)`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 10px;
  margin-top: 15px;
  border-radius: 20px;
  gap: 10px;
  width: 100%;
  background-color: #60a658;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
`;

const CancelButtonText = styled.Text`
  font-size: 16px;
  color: white;
  font-weight: bold;
`;

export default function CardMyEvents(props: CardProps) {
  const {
    title,
    startDate,
    headerImage,
    status,
    id,
    setIdToCancel,
    setShowCancelAlert,
    setIdToConfirm,
    setShowConfirmAlert,
  } = props;

  const isPast = () => startDate < new Date().toISOString();

  return (
    <CardContainer isPast={isPast()}>
      <CardImage source={{ uri: headerImage }} />
      <CardTextContainer>
        <CardTitle>{title}</CardTitle>
        <TextLine>
          <FontAwesome5 name="calendar" size={16} />
          <CardText>{parseDate(startDate)}</CardText>
        </TextLine>
        <ButtonsContainer>
          {status === "Invited" && !isPast() && (
            <ConfirmButton
              onPress={() => {
                setIdToConfirm(id);
                setShowConfirmAlert(true);
              }}
            >
              <CancelButtonText>Confirm participation</CancelButtonText>
            </ConfirmButton>
          )}
          {status !== "Cancelled" &&
            status !== "Rejected" &&
            status !== "Invalid" &&
            !isPast() && (
              <CancelButton
                onPress={() => {
                  setIdToCancel(id);
                  setShowCancelAlert(true);
                }}
              >
                <CancelButtonText>Cancel participation</CancelButtonText>
              </CancelButton>
            )}
        </ButtonsContainer>
      </CardTextContainer>
      <AbsoluteChip
        name={status}
        backgroundColor={getColorForApplicationStatus(status)}
      />
    </CardContainer>
  );
}
