import React, { useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import {
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
} from "react-native";
import Toast from "react-native-toast-message";
import { router } from "expo-router";
import LoadingPage from "../../../components/Pages/LodingPage";
import { createEvent } from "../../../utils/api/axiosEvents";
import { getToken } from "../../../utils/sessionCalls";
import EventForm from "../../../components/componentsStyled/Forms/EventForm";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

export default function CreatePage() {
  const [inputs, setInputs] = useState({
    name: "",
    url: "",
    description: "",
    startDate: "",
    endDate: "",
    location: "",
    maxParticipants: "",
    attritionRate: "",
    minAge: "",
    onlyForStudents: false,
    headerImage: "",
    openForParticipants: true,
  });

  const [loading, setLoading] = React.useState(false);

  const createTheEvent = () => {
    setLoading(true);
    const fetchData = async () => {
      const token = await getToken();
      return createEvent(token || "", inputs);
    };

    fetchData().then((response) => {
      setLoading(false);
      if (response.error) {
        Toast.show({
          type: "error",
          text1: "There is an error!!",
          text2: response.error,
        });
      } else {
        router.push("/");
      }
    });
  };

  return (
    <Container>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        keyboardVerticalOffset={100}
      >
        <ScrollView contentContainerStyle={{ padding: 30 }}>
          {loading ? (
            <LoadingPage />
          ) : (
            <EventForm
              inputs={inputs}
              setInputs={setInputs}
              createTheEvent={createTheEvent}
            />
          )}
        </ScrollView>
      </KeyboardAvoidingView>
      <Toast />
    </Container>
  );
}
