import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import { FontAwesome5 } from "@expo/vector-icons";
import { Pressable } from "react-native";
import {
  getColorForApplicationStatus,
  parseDate,
} from "../utils/util-functions";

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

const CardContainer = styled.View<{ isPast: boolean }>`
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
  border-radius: 20px;
  margin: 10px;
  width: 300px;
  opacity: ${(props: { isPast: boolean }) => (props.isPast ? 0.5 : 1)};
`;

const CardImage = styled.Image`
  height: 200px;
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

const TagContainer = styled.View`
  display: flex;
  width: 100%;
  margin-top: 20px;
  align-items: flex-end;
  position: absolute;
  right: 15px;
`;

const TagStatus = styled.View<{ backgroundColor: string }>`
  border: 2px solid
    ${(props: { backgroundColor: string }) => props.backgroundColor};
  background-color: ${(props: { backgroundColor: string }) =>
    props.backgroundColor};
  padding: 5px 10px;
  border-radius: 20px;
  text-align: center;
`;

const TagText = styled.Text`
  font-weight: bold;
  font-size: 16px;
`;

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
      <TagContainer>
        <TagStatus backgroundColor={getColorForApplicationStatus(status)}>
          <TagText>{status}</TagText>
        </TagStatus>
      </TagContainer>
    </CardContainer>
  );
}
