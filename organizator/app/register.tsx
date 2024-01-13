import React, { useEffect, useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import {
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
  View,
} from "react-native";

import { router } from "expo-router";
import Toast from "react-native-toast-message";
import Input from "../components/componentsStyled/Forms/Input";
import Button from "../components/componentsStyled/Buttons/ButtonWithIcon";
import { registerUser } from "../utils/api/axiosUsers";
import { RegisterResponse } from "../utils/interfaces/Users";
import { getToken } from "../utils/sessionCalls";
import LoadingPage from "../components/Pages/LodingPage";
import { checkDateBirth, checkDateGraduation } from "../utils/util-functions";
import FilterButton from "../components/componentsStyled/Buttons/FilterButtons";
import InputLabel from "../components/componentsStyled/Forms/InputLabel";
import {
  SubTitle,
  Title,
} from "../components/componentsStyled/Shared/TextStyles";
import {
  BottomScreenContainer,
  MaxWidthUseScreen,
} from "../components/componentsStyled/Shared/ContainerStyles";
import {
  handleError,
  handleOnChange,
} from "../components/componentsStyled/Forms/utilFunctions";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

const ButtonsWSContainer = styled(View)`
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  margin-bottom: 20px;
`;

export default function RegisterPage() {
  const [inputs, setInputs] = useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
    firstName: "",
    lastName: "",
    bio: "",
    dateOfBirth: "",
    currentJobRole: "",
    university: "",
    degree: "",
    graduationYear: "",
  });
  const [errors, setErrors] = React.useState({
    username: undefined,
    email: undefined,
    password: undefined,
    passwordConfirm: undefined,
    firstName: undefined,
    lastName: undefined,
    bio: undefined,
    dateOfBirth: undefined,
    currentJobRole: undefined,
    university: undefined,
    degree: undefined,
    graduationYear: undefined,
  });
  const [loading, setLoading] = React.useState(false);
  const [isWorking, setIsWorking] = React.useState(false);
  const [isStudying, setIsStudying] = React.useState(true);
  const [active, setActive] = React.useState({
    study: true,
    work: false,
    nothing: false,
  });

  useEffect(() => {
    getToken().then((token) => {
      if (token) {
        router.replace("/");
      }
    });
  }, []);

  const validate = () => {
    let isValid = true;

    if (!inputs.username) {
      handleError("Please enter your username", "username", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "username", setErrors);
    }

    if (!inputs.email) {
      handleError("Please enter an email address", "email", setErrors);
      isValid = false;
    } else if (!inputs.email.match(/\S+@\S+\.\S+/)) {
      handleError("Please enter a valid email address", "email", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "email", setErrors);
    }

    if (!inputs.password) {
      handleError("Please enter a password", "password", setErrors);
      isValid = false;
    } else if (inputs.password.length < 8) {
      handleError("Minimum password length is 8", "password", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "password", setErrors);
    }

    if (!inputs.passwordConfirm) {
      handleError(
        "Please enter confirm password",
        "passwordConfirm",
        setErrors,
      );
      isValid = false;
    } else if (inputs.passwordConfirm !== inputs.password) {
      handleError(
        "Password confirmation does not match",
        "passwordConfirm",
        setErrors,
      );
      isValid = false;
    } else {
      handleError(undefined, "passwordConfirm", setErrors);
    }

    if (!inputs.firstName) {
      handleError("Please enter your first name", "firstName", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "firstName", setErrors);
    }

    if (!inputs.lastName) {
      handleError("Please enter your last name", "lastName", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "lastName", setErrors);
    }

    if (!inputs.dateOfBirth) {
      handleError("Please enter your date birth", "dateOfBirth", setErrors);
      isValid = false;
    } else {
      const dateChecker = checkDateBirth(inputs.dateOfBirth);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "dateOfBirth", setErrors);
        isValid = false;
      } else {
        handleError(undefined, "dateOfBirth", setErrors);
      }
    }

    if (!inputs.bio) {
      handleError("Please enter your bio", "bio", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "bio", setErrors);
    }

    if (!inputs.graduationYear && isStudying) {
      handleError(
        "Please enter your graduation year",
        "graduationYear",
        setErrors,
      );
      isValid = false;
    } else {
      const dateChecker = checkDateGraduation(inputs.graduationYear);
      if (!dateChecker.valid && isStudying) {
        handleError(dateChecker.error, "graduationYear", setErrors);
        isValid = false;
      } else {
        handleError(undefined, "graduationYear", setErrors);
      }
    }

    if (!inputs.currentJobRole && isWorking) {
      handleError(
        "Please enter your current job role",
        "currentJobRole",
        setErrors,
      );
      isValid = false;
    } else {
      handleError(undefined, "currentJobRole", setErrors);
    }

    if (!inputs.university && isStudying) {
      handleError("Please enter your university", "university", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "university", setErrors);
    }

    if (!inputs.degree && isStudying) {
      handleError("Please enter your degree", "degree", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "degree", setErrors);
    }

    if (isValid) {
      register();
    } else {
      Toast.show({
        type: "error",
        text1: "Form not filled correctly",
        text2: "Please check all the fields are correctly field",
      });
    }
  };

  const register = () => {
    setLoading(true);
    registerUser(inputs, isWorking, isStudying).then(
      (response: RegisterResponse) => {
        setLoading(false);
        if (response.error) {
          Toast.show({
            type: "error",
            text1: "Error",
            text2: response.error,
            visibilityTime: 8000,
          });
        } else {
          router.replace("/login");
        }
      },
    );
  };

  return (
    <Container>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        keyboardVerticalOffset={100}
      >
        <ScrollView
          contentContainerStyle={{
            paddingVertical: 30,
            paddingHorizontal: 20,
          }}
        >
          {loading ? (
            <LoadingPage />
          ) : (
            <MaxWidthUseScreen>
              <Title>Welcome on board</Title>
              <SubTitle>
                To be able to register in our events we need some information
                about you!
              </SubTitle>
              <Input
                label="Username"
                iconName="user"
                required
                value={inputs.username}
                onChangeText={(text) =>
                  handleOnChange(text, "username", setInputs)
                }
                error={errors.username}
              />
              <Input
                label="Email"
                iconName="at"
                required
                value={inputs.email}
                onChangeText={(text) =>
                  handleOnChange(text, "email", setInputs)
                }
                error={errors.email}
                keyboardType="email-address"
              />
              <Input
                label="Password"
                iconName="lock"
                required
                value={inputs.password}
                onChangeText={(text) =>
                  handleOnChange(text, "password", setInputs)
                }
                error={errors.password}
                password
              />
              <Input
                label="Confirm your password"
                iconName="lock"
                required
                value={inputs.passwordConfirm}
                onChangeText={(text) =>
                  handleOnChange(text, "passwordConfirm", setInputs)
                }
                error={errors.passwordConfirm}
                password
              />
              <Input
                label="First Name"
                iconName="id-badge"
                required
                value={inputs.firstName}
                onChangeText={(text) =>
                  handleOnChange(text, "firstName", setInputs)
                }
                error={errors.firstName}
              />
              <Input
                label="Last Name"
                iconName="id-badge"
                required
                value={inputs.lastName}
                onChangeText={(text) =>
                  handleOnChange(text, "lastName", setInputs)
                }
                error={errors.lastName}
              />
              <Input
                label="Date of birth"
                iconName="calendar"
                required
                value={inputs.dateOfBirth}
                onChangeText={(text) =>
                  handleOnChange(text, "dateOfBirth", setInputs)
                }
                placeholder="DD/MM/YYYY"
                placeholderTextColor="#969696"
                error={errors.dateOfBirth}
              />
              <Input
                label="Biography"
                iconName="pencil"
                required
                multiline
                numberOfLines={3}
                value={inputs.bio}
                onChangeText={(text) => handleOnChange(text, "bio", setInputs)}
                error={errors.bio}
              />

              <InputLabel
                label="Currently I'm... (select one of the options)"
                required
              />
              <ButtonsWSContainer>
                <FilterButton
                  title="Studying"
                  onPress={() => {
                    setActive({ study: true, work: false, nothing: false });
                    setIsStudying(true);
                    setIsWorking(false);
                  }}
                  color="dimgray"
                  active={active.study}
                />
                <FilterButton
                  title="Working"
                  onPress={() => {
                    setActive({ study: false, work: true, nothing: false });
                    setIsStudying(false);
                    setIsWorking(true);
                  }}
                  color="dimgray"
                  active={active.work}
                />
                <FilterButton
                  title="Another thing"
                  onPress={() => {
                    setActive({ study: false, work: false, nothing: true });
                    setIsStudying(false);
                    setIsWorking(false);
                  }}
                  color="dimgray"
                  active={active.nothing}
                />
              </ButtonsWSContainer>

              {isWorking && (
                <Input
                  label="Current Job Role"
                  iconName="briefcase"
                  required
                  value={inputs.currentJobRole}
                  onChangeText={(text) =>
                    handleOnChange(text, "currentJobRole", setInputs)
                  }
                  error={errors.currentJobRole}
                />
              )}

              {isStudying && (
                <>
                  <Input
                    label="University"
                    iconName="university"
                    required
                    value={inputs.university}
                    onChangeText={(text) =>
                      handleOnChange(text, "university", setInputs)
                    }
                    error={errors.university}
                  />
                  <Input
                    label="Degree"
                    iconName="book"
                    required
                    value={inputs.degree}
                    onChangeText={(text) =>
                      handleOnChange(text, "degree", setInputs)
                    }
                    error={errors.degree}
                  />
                  <Input
                    label="Graduation year"
                    iconName="graduation-cap"
                    required
                    value={inputs.graduationYear}
                    onChangeText={(text) =>
                      handleOnChange(text, "graduationYear", setInputs)
                    }
                    placeholder="DD/MM/YYYY"
                    placeholderTextColor="#969696"
                    error={errors.graduationYear}
                  />
                </>
              )}
              <Button
                title="Register"
                onPress={validate}
                color="#58a659"
                iconName="check-square-o"
              />
            </MaxWidthUseScreen>
          )}
        </ScrollView>
      </KeyboardAvoidingView>
      <Toast />
    </Container>
  );
}
