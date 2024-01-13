import React from "react";
import { FontAwesome5 } from "@expo/vector-icons";
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
import Button from "../Buttons/ButtonWithIcon";
import { systemColors } from "../tokens";
import { ButtonsRowContainer } from "../Shared/ContainerStyles";

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
        <ButtonsRowContainer marginTop="25px">
          {status === "Invited" && !isPast() && (
            <Button
              title="Confirm"
              onPress={() => {
                setIdToConfirm(id);
                setShowConfirmAlert(true);
              }}
              color={systemColors.accept}
            />
          )}
          {status !== "Cancelled" &&
            status !== "Rejected" &&
            status !== "Invalid" &&
            !isPast() && (
              <Button
                title="Cancel"
                onPress={() => {
                  setIdToCancel(id);
                  setShowCancelAlert(true);
                }}
                color={systemColors.destroy}
              />
            )}
        </ButtonsRowContainer>
      </CardTextContainer>
      <AbsoluteChip
        name={status}
        backgroundColor={getColorForApplicationStatus(status)}
      />
    </CardContainer>
  );
}
