import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import { FontAwesome5 } from "@expo/vector-icons";
import { Pressable, Text } from "react-native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import Toast from "react-native-toast-message";
import {
  getColorForApplicationStatus,
  parseDate,
} from "../utils/util-functions";
import { getToken } from "../utils/sessionCalls";
import { getUserRole } from "../utils/api/axiosUsers";
import { cancelApplication } from "../utils/api/axiosApplications";

interface CardProps {
  title: string;
  startDate: string;
  headerImage: string;
  status: string;
  id: string;
  trigger: boolean;
  setTrigger: (trigger: boolean) => void;
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

const ButtonsContainer = styled.View`
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
`;

const CancelButton = styled(Pressable)`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 10px 30px;
  margin-top: 20px;
  border-radius: 20px;
  gap: 10px;
  background-color: #a65858;
  width: 50%;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
`;

const CancelButtonText = styled.Text`
  font-size: 16px;
  color: white;
  font-weight: bold;
`;

export default function CardMyEvents(props: CardProps) {
  const { title, startDate, headerImage, status, id, trigger, setTrigger } =
    props;

  const isPast = () => startDate < new Date().toISOString();

  function cancel() {
    const fetchData = async () => {
      const t = await getToken();
      return cancelApplication(t || "", id);
    };

    fetchData().then((response) => {
      if (response.error) {
        Toast.show({
          type: "error",
          text1: "Error",
          text2: response.error,
          visibilityTime: 8000,
        });
      } else {
        setTrigger(!trigger);
        Toast.show({
          type: "success",
          text1: "Success",
          text2: "Your application has been cancelled!",
          visibilityTime: 8000,
        });
      }
    });
  }

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
          <ButtonsContainer>
            {status !== "Cancelled" &&
              status !== "Rejected" &&
              status !== "Invalid" && (
                <CancelButton onPress={() => cancel()}>
                  <FontAwesome name="close" size={16} color="white" />
                  <CancelButtonText>Cancel</CancelButtonText>
                </CancelButton>
              )}
          </ButtonsContainer>
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
