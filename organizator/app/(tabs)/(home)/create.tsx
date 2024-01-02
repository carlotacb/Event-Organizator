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
import {
  checkDate,
  checkDateRange,
  checkURL,
  dateToPlainString,
} from "../../../utils/util-functions";

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
    let isValid = true;

    if (!inputs.name) {
      handleError("Please enter a name for the event", "name");
      isValid = false;
    } else {
      handleError(undefined, "name");
    }

    if (!inputs.url) {
      handleError("Please enter a url for the event", "url");
      isValid = false;
    } else {
      const urlChecker = checkURL(inputs.url);
      if (!urlChecker.valid) {
        handleError(urlChecker.error, "url");
        isValid = false;
      } else {
        handleError(undefined, "url");
      }
    }

    if (!inputs.description) {
      handleError("Please enter a description for the event", "description");
      isValid = false;
    } else {
      handleError(undefined, "description");
    }

    if (!inputs.startDate) {
      handleError("Please enter a starting date for the event", "startDate");
      isValid = false;
    } else {
      const dateChecker = checkDate(inputs.startDate);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "startDate");
        isValid = false;
      } else {
        const today = new Date();
        const validRange = checkDateRange(
          dateToPlainString(today),
          inputs.startDate,
        );
        if (!validRange.valid) {
          handleError(validRange.error, "startDate");
          isValid = false;
        } else {
          handleError(undefined, "startDate");
        }
      }
    }

    if (!inputs.endDate) {
      handleError("Please enter a ending date for the event", "endDate");
      isValid = false;
    } else {
      const dateChecker = checkDate(inputs.endDate);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "endDate");
        isValid = false;
      } else {
        const validRange = checkDateRange(inputs.startDate, inputs.endDate);
        if (!validRange.valid) {
          handleError(validRange.error, "endDate");
          isValid = false;
        } else {
          handleError(undefined, "endDate");
        }
      }
    }

    if (!inputs.location) {
      handleError("Please enter a location for the event", "location");
      isValid = false;
    } else {
      handleError(undefined, "location");
    }

    if (!inputs.headerImage) {
      handleError("Please enter a header image for the event", "headerImage");
      isValid = false;
    } else {
      handleError(undefined, "headerImage");
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
              placeholder="https://www.example.com"
              placeholderTextColor="#969696"
              error={errors.url}
            />
            <Input
              label="Start date"
              iconName="hourglass-start"
              required
              value={inputs.startDate}
              onChangeText={(text) => handleOnChange(text, "startDate")}
              placeholder="DD/MM/YYYY HH:MM"
              placeholderTextColor="#969696"
              error={errors.startDate}
            />
            <Input
              label="End date"
              iconName="hourglass-end"
              required
              value={inputs.endDate}
              onChangeText={(text) => handleOnChange(text, "endDate")}
              placeholder="DD/MM/YYYY HH:MM"
              placeholderTextColor="#969696"
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
              placeholder="Explain a bit about what's the event about, you can write as much as you want!"
              placeholderTextColor="#969696"
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
