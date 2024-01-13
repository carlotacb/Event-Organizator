import React from "react";
import { View } from "react-native";
import { handleError, handleOnChange } from "./utilFunctions";
import {
  checkDateRange,
  checkDateWithTime,
  checkURL,
  dateToPlainString,
} from "../../../utils/util-functions";
import Input from "./Input";
import InputLabel from "./InputLabel";
import FilterButton from "../Buttons/FilterButtons";
import { ButtonsRowContainer } from "../Shared/ContainerStyles";
import Button from "../Buttons/ButtonWithIcon";

interface EventFormProps {
  inputs: {
    name: string;
    url: string;
    description: string;
    startDate: string;
    endDate: string;
    location: string;
    maxParticipants: string;
    attritionRate: string;
    minAge: string;
    onlyForStudents: boolean;
    headerImage: string;
    openForParticipants: boolean;
  };
  setInputs: React.Dispatch<
    React.SetStateAction<{
      name: string;
      url: string;
      description: string;
      startDate: string;
      endDate: string;
      location: string;
      maxParticipants: string;
      attritionRate: string;
      minAge: string;
      onlyForStudents: boolean;
      headerImage: string;
      openForParticipants: boolean;
    }>
  >;
  createTheEvent: () => void;
  isUpdate?: boolean;
}

export default function EventForm(props: EventFormProps) {
  const { inputs, setInputs, createTheEvent, isUpdate } = props;
  const [errors, setErrors] = React.useState({
    name: undefined,
    url: undefined,
    description: undefined,
    startDate: undefined,
    endDate: undefined,
    location: undefined,
    maxParticipants: undefined,
    attritionRate: undefined,
    minAge: undefined,
    headerImage: undefined,
  });

  const validate = () => {
    let isValid = true;

    if (!inputs.name) {
      handleError("Please enter a name for the event", "name", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "name", setErrors);
    }

    if (!inputs.url) {
      handleError("Please enter a url for the event", "url", setErrors);
      isValid = false;
    } else {
      const urlChecker = checkURL(inputs.url);
      if (!urlChecker.valid) {
        handleError(urlChecker.error, "url", setErrors);
        isValid = false;
      } else {
        handleError(undefined, "url", setErrors);
      }
    }

    if (!inputs.description) {
      handleError(
        "Please enter a description for the event",
        "description",
        setErrors,
      );
      isValid = false;
    } else {
      handleError(undefined, "description", setErrors);
    }

    if (!inputs.startDate) {
      handleError(
        "Please enter a starting date for the event",
        "startDate",
        setErrors,
      );
      isValid = false;
    } else {
      const dateChecker = checkDateWithTime(inputs.startDate);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "startDate", setErrors);
        isValid = false;
      } else {
        const today = new Date();
        const validRange = checkDateRange(
          dateToPlainString(today),
          inputs.startDate,
        );
        if (!validRange.valid) {
          handleError(validRange.error, "startDate", setErrors);
          isValid = false;
        } else {
          handleError(undefined, "startDate", setErrors);
        }
      }
    }

    if (!inputs.endDate) {
      handleError(
        "Please enter a ending date for the event",
        "endDate",
        setErrors,
      );
      isValid = false;
    } else {
      const dateChecker = checkDateWithTime(inputs.endDate);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "endDate", setErrors);
        isValid = false;
      } else {
        const validRange = checkDateRange(inputs.startDate, inputs.endDate);
        if (!validRange.valid) {
          handleError(validRange.error, "endDate", setErrors);
          isValid = false;
        } else {
          handleError(undefined, "endDate", setErrors);
        }
      }
    }

    if (!inputs.location) {
      handleError(
        "Please enter a location for the event",
        "location",
        setErrors,
      );
      isValid = false;
    } else {
      handleError(undefined, "location", setErrors);
    }

    if (!inputs.maxParticipants) {
      handleError(
        "Please enter a max participants for the event",
        "maxParticipants",
        setErrors,
      );
      isValid = false;
    } else {
      const isNum = /^\d+$/.test(inputs.maxParticipants);
      if (!isNum) {
        handleError(
          "Please enter a valid number",
          "maxParticipants",
          setErrors,
        );
        isValid = false;
      } else {
        handleError(undefined, "maxParticipants", setErrors);
      }
    }

    if (!inputs.attritionRate) {
      handleError(
        "Please enter the expected attrition rate for the event",
        "attritionRate",
        setErrors,
      );
      isValid = false;
    } else {
      const isNum = /^\d+$/.test(inputs.attritionRate);
      if (!isNum) {
        handleError("Please enter a valid number", "attritionRate", setErrors);
        isValid = false;
      } else {
        handleError(undefined, "attritionRate", setErrors);
      }
    }

    if (!inputs.minAge) {
      handleError(
        "Please enter the minimum age to participate in the event",
        "minAge",
        setErrors,
      );
      isValid = false;
    } else {
      const isNum = /^\d+$/.test(inputs.minAge);
      if (!isNum) {
        handleError("Please enter a valid number", "minAge", setErrors);
        isValid = false;
      } else {
        handleError(undefined, "minAge", setErrors);
      }
    }

    if (!inputs.headerImage) {
      handleError(
        "Please enter a header image for the event",
        "headerImage",
        setErrors,
      );
      isValid = false;
    } else {
      handleError(undefined, "headerImage", setErrors);
    }

    if (isValid) {
      createTheEvent();
    }
  };

  return (
    <>
      <Input
        label="Event name"
        iconName="tag"
        required
        value={inputs.name}
        onChangeText={(text) => handleOnChange(text, "name", setInputs)}
        error={errors.name}
      />
      <Input
        label="Webpage url"
        iconName="link"
        required
        value={inputs.url}
        onChangeText={(text) => handleOnChange(text, "url", setInputs)}
        placeholder="https://www.example.com"
        placeholderTextColor="#969696"
        error={errors.url}
      />
      <Input
        label="Start date"
        iconName="hourglass-start"
        required
        value={inputs.startDate}
        onChangeText={(text) => handleOnChange(text, "startDate", setInputs)}
        placeholder="DD/MM/YYYY HH:MM"
        placeholderTextColor="#969696"
        error={errors.startDate}
      />
      <Input
        label="End date"
        iconName="hourglass-end"
        required
        value={inputs.endDate}
        onChangeText={(text) => handleOnChange(text, "endDate", setInputs)}
        placeholder="DD/MM/YYYY HH:MM"
        placeholderTextColor="#969696"
        error={errors.endDate}
      />
      <Input
        label="Location"
        iconName="map-marker"
        required
        value={inputs.location}
        onChangeText={(text) => handleOnChange(text, "location", setInputs)}
        error={errors.location}
      />
      <View
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
        }}
      >
        <Input
          label="Max participants"
          iconName="users"
          required
          value={inputs.maxParticipants}
          onChangeText={(text) =>
            handleOnChange(text, "maxParticipants", setInputs)
          }
          error={errors.maxParticipants}
          width="48%"
          inputMode="numeric"
          keyboardType="numeric"
        />
        <Input
          label="Attrition rate (%)"
          iconName="percent"
          required
          value={inputs.attritionRate}
          onChangeText={(text) =>
            handleOnChange(text, "attritionRate", setInputs)
          }
          error={errors.attritionRate}
          width="48%"
          inputMode="numeric"
          keyboardType="numeric"
        />
      </View>
      <View
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Input
          label="Minimum age"
          iconName="calendar-minus-o"
          required
          value={inputs.minAge}
          onChangeText={(text) => handleOnChange(text, "minAge", setInputs)}
          error={errors.minAge}
          width="48%"
          inputMode="numeric"
          keyboardType="numeric"
        />
        <View
          style={{
            display: "flex",
            flexDirection: "column",
            width: "48%",
            marginBottom: 20,
          }}
        >
          <InputLabel label="Is only for students?" required />
          <View
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
            }}
          >
            <FilterButton
              onPress={() => {
                setInputs((prevState) => ({
                  ...prevState,
                  onlyForStudents: true,
                }));
              }}
              color="dimgray"
              iconName="graduation-cap"
              title="Yep"
              active={inputs.onlyForStudents}
            />
            <FilterButton
              onPress={() => {
                setInputs((prevState) => ({
                  ...prevState,
                  onlyForStudents: false,
                }));
              }}
              color="dimgray"
              iconName="globe"
              title="Nop"
              active={!inputs.onlyForStudents}
            />
          </View>
        </View>
      </View>
      {!isUpdate && (
        <Input
          label="Header image link"
          iconName="image"
          required
          value={inputs.headerImage}
          onChangeText={(text) =>
            handleOnChange(text, "headerImage", setInputs)
          }
          error={errors.headerImage}
        />
      )}
      <Input
        label="Description"
        iconName="pencil"
        required
        multiline
        numberOfLines={4}
        value={inputs.description}
        onChangeText={(text) => handleOnChange(text, "description", setInputs)}
        placeholder="Explain a bit about what's the event about, you can write as much as you want!"
        placeholderTextColor="#969696"
        error={errors.description}
      />

      <View
        style={{
          display: "flex",
          flexDirection: "column",
        }}
      >
        <InputLabel label="Is open for participants to apply?" required />
        <View
          style={{
            display: "flex",
            flexDirection: "row",
          }}
        >
          <FilterButton
            onPress={() => {
              setInputs((prevState) => ({
                ...prevState,
                openForParticipants: true,
              }));
            }}
            color="dimgray"
            iconName="check"
            title="Yep"
            active={inputs.openForParticipants}
          />
          <FilterButton
            onPress={() => {
              setInputs((prevState) => ({
                ...prevState,
                openForParticipants: false,
              }));
            }}
            color="dimgray"
            iconName="close"
            title="Nop"
            active={!inputs.openForParticipants}
          />
        </View>
      </View>

      <ButtonsRowContainer marginTop="30px">
        <Button
          title={isUpdate ? "Save" : "Create"}
          onPress={validate}
          color="#58a659"
          iconName="save"
        />
      </ButtonsRowContainer>
    </>
  );
}
