import React, { useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import { SafeAreaView, ScrollView, View } from "react-native";
import Toast from "react-native-toast-message";
import { router } from "expo-router";
import LoadingPage from "../../../components/LodingPage";
import Input from "../../../components/Input";
import Button from "../../../components/ButtonWithIcon";
import { createEvent } from "../../../utils/api/axiosEvents";
import { createEventResponse } from "../../../utils/interfaces/Events";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

const ButtonContainer = styled(View)`
  display: flex;
  margin-top: 15px;
  align-items: center;
`;

export default function CreatePage() {
  const [inputs, setInputs] = useState({
    name: "",
    url: "",
    description: "",
    startDate: "",
    endDate: "",
    location: "",
    headerImage: "",
  });
  const [errors, setErrors] = React.useState({
    name: undefined,
    url: undefined,
    description: undefined,
    startDate: undefined,
    endDate: undefined,
    location: undefined,
    headerImage: undefined,
  });
  const [loading, setLoading] = React.useState(false);

  const handleOnChange = (text: string, input: string) => {
    setInputs((prevState) => ({ ...prevState, [input]: text }));
  };
  const handleError = (text: string | undefined, input: string) => {
    setErrors((prevState) => ({ ...prevState, [input]: text }));
  };

  const validate = () => {
    let isValid = false;

    if (!inputs.name) {
      handleError("Please enter a name for the event", "name");
    } else {
      handleError(undefined, "name");
    }

    if (!inputs.url) {
      handleError("Please enter a url for the event", "url");
    } else {
      handleError(undefined, "url");
    }

    if (!inputs.description) {
      handleError("Please enter a description for the event", "description");
    } else {
      handleError(undefined, "description");
    }

    if (!inputs.startDate) {
      handleError("Please enter a starting date for the event", "startDate");
    } else {
      handleError(undefined, "startDate");
    }

    if (!inputs.endDate) {
      handleError("Please enter a ending date for the event", "endDate");
    } else {
      handleError(undefined, "endDate");
    }

    if (!inputs.location) {
      handleError("Please enter a location for the event", "location");
    } else {
      handleError(undefined, "location");
    }

    if (!inputs.headerImage) {
      handleError("Please enter a header image for the event", "headerImage");
    } else {
      handleError(undefined, "headerImage");
    }

    if (
      errors.name === undefined &&
      errors.url === undefined &&
      errors.description === undefined &&
      errors.startDate === undefined &&
      errors.endDate === undefined &&
      errors.location === undefined &&
      errors.headerImage === undefined
    ) {
      isValid = true;
    }

    if (isValid) {
      createTheEvent();
    }
  };

  const createTheEvent = () => {
    setLoading(true);
    createEvent(inputs).then((response: createEventResponse) => {
      setLoading(false);
      if (response.error) {
        Toast.show({
          type: "error",
          text1: "There is an error!!",
          text2: response.error,
        });
      } else {
        router.replace("/");
      }
    });
  };

  return (
    <Container>
      <ScrollView contentContainerStyle={{ padding: 30 }}>
        {loading ? (
          <LoadingPage />
        ) : (
          <>
            <Input
              label="Event name"
              iconName="tag"
              required
              value={inputs.name}
              onChangeText={(text) => handleOnChange(text, "name")}
              error={errors.name}
            />
            <Input
              label="Webpage url"
              iconName="link"
              required
              value={inputs.url}
              onChangeText={(text) => handleOnChange(text, "url")}
              error={errors.url}
            />
            <Input
              label="Start date"
              iconName="hourglass-start"
              required
              value={inputs.startDate}
              onChangeText={(text) => handleOnChange(text, "startDate")}
              error={errors.startDate}
            />
            <Input
              label="End date"
              iconName="hourglass-end"
              required
              value={inputs.endDate}
              onChangeText={(text) => handleOnChange(text, "endDate")}
              error={errors.endDate}
            />
            <Input
              label="Location"
              iconName="map-marker"
              required
              value={inputs.location}
              onChangeText={(text) => handleOnChange(text, "location")}
              error={errors.location}
            />
            <Input
              label="Header image link"
              iconName="image"
              required
              value={inputs.headerImage}
              onChangeText={(text) => handleOnChange(text, "headerImage")}
              error={errors.headerImage}
            />
            <Input
              label="Description"
              iconName="pencil"
              required
              multiline
              numberOfLines={4}
              value={inputs.description}
              onChangeText={(text) => handleOnChange(text, "description")}
              error={errors.description}
            />

            <ButtonContainer>
              <Button
                title="Create"
                onPress={validate}
                color="#58a659"
                iconName="save"
              />
            </ButtonContainer>
          </>
        )}
        <Toast />
      </ScrollView>
    </Container>
  );
}
