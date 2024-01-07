import React, { useEffect, useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import { SafeAreaView, Text, ScrollView, View } from "react-native";

import { router } from "expo-router";
import Toast from "react-native-toast-message";
import Input from "../components/Input";
import Button from "../components/ButtonWithIcon";
import { registerUser } from "../utils/api/axiosUsers";
import { RegisterResponse } from "../utils/interfaces/Users";
import { getToken } from "../utils/sessionCalls";
import LoadingPage from "../components/LodingPage";
import { checkDateBirth, checkDateGraduation } from "../utils/util-functions";
import FilterButton from "../components/FilterButtons";
import InputLabel from "../components/InputLabel";

const Container = styled(SafeAreaView)`
  padding: 50px 40px;
  background-color: white;
`;

const Title = styled(Text)`
  font-size: 30px;
  font-weight: bold;
  color: black;
  text-align: center;
  text-transform: uppercase;
`;

const SubTitle = styled(Text)`
  font-size: 15px;
  color: gray;
  margin: 10px 0 30px 0;
  text-align: center;
`;

const ButtonContainer = styled(View)`
  display: flex;
  margin-top: 15px;
  align-items: center;
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
  });

  const validate = () => {
    let isValid = true;

    if (!inputs.username) {
      handleError("Please enter your username", "username");
      isValid = false;
    } else {
      handleError(undefined, "username");
    }

    if (!inputs.email) {
      handleError("Please enter an email address", "email");
      isValid = false;
    } else if (!inputs.email.match(/\S+@\S+\.\S+/)) {
      handleError("Please enter a valid email address", "email");
      isValid = false;
    } else {
      handleError(undefined, "email");
    }

    if (!inputs.password) {
      handleError("Please enter a password", "password");
      isValid = false;
    } else if (inputs.password.length < 8) {
      handleError("Minimum password length is 8", "password");
      isValid = false;
    } else {
      handleError(undefined, "password");
    }

    if (!inputs.passwordConfirm) {
      handleError("Please enter confirm password", "passwordConfirm");
      isValid = false;
    } else if (inputs.passwordConfirm !== inputs.password) {
      handleError("Password confirmation does not match", "passwordConfirm");
      isValid = false;
    } else {
      handleError(undefined, "passwordConfirm");
    }

    if (!inputs.firstName) {
      handleError("Please enter your first name", "firstName");
      isValid = false;
    } else {
      handleError(undefined, "firstName");
    }

    if (!inputs.lastName) {
      handleError("Please enter your last name", "lastName");
      isValid = false;
    } else {
      handleError(undefined, "lastName");
    }

    if (!inputs.dateOfBirth) {
      handleError("Please enter your date birth", "dateOfBirth");
      isValid = false;
    } else {
      const dateChecker = checkDateBirth(inputs.dateOfBirth);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "dateOfBirth");
        isValid = false;
      } else {
        handleError(undefined, "dateOfBirth");
      }
    }

    if (!inputs.bio) {
      handleError("Please enter your bio", "bio");
      isValid = false;
    } else {
      handleError(undefined, "bio");
    }

    if (!inputs.graduationYear && isStudying) {
      handleError("Please enter your graduation year", "graduationYear");
      isValid = false;
    } else {
      const dateChecker = checkDateGraduation(inputs.graduationYear);
      if (!dateChecker.valid && isStudying) {
        handleError(dateChecker.error, "graduationYear");
        isValid = false;
      } else {
        handleError(undefined, "graduationYear");
      }
    }

    if (!inputs.currentJobRole && isWorking) {
      handleError("Please enter your current job role", "currentJobRole");
      isValid = false;
    } else {
      handleError(undefined, "currentJobRole");
    }

    if (!inputs.university && isStudying) {
      handleError("Please enter your university", "university");
      isValid = false;
    } else {
      handleError(undefined, "university");
    }

    if (!inputs.degree && isStudying) {
      handleError("Please enter your degree", "degree");
      isValid = false;
    } else {
      handleError(undefined, "degree");
    }

    if (isValid) {
      register();
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

  const handleOnChange = (text: string, input: string) => {
    setInputs((prevState) => ({ ...prevState, [input]: text }));
  };
  const handleError = (text: string | undefined, input: string) => {
    setErrors((prevState) => ({ ...prevState, [input]: text }));
  };

  return (
    <Container>
      <ScrollView
        contentContainerStyle={{ paddingVertical: 30, paddingHorizontal: 20 }}
      >
        {loading ? (
          <LoadingPage />
        ) : (
          <>
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
              onChangeText={(text) => handleOnChange(text, "username")}
              error={errors.username}
            />
            <Input
              label="Email"
              iconName="at"
              required
              value={inputs.email}
              onChangeText={(text) => handleOnChange(text, "email")}
              error={errors.email}
              keyboardType="email-address"
            />
            <Input
              label="Password"
              iconName="lock"
              required
              value={inputs.password}
              onChangeText={(text) => handleOnChange(text, "password")}
              error={errors.password}
              password
            />
            <Input
              label="Confirm your password"
              iconName="lock"
              required
              value={inputs.passwordConfirm}
              onChangeText={(text) => handleOnChange(text, "passwordConfirm")}
              error={errors.passwordConfirm}
              password
            />
            <Input
              label="First Name"
              iconName="id-badge"
              required
              value={inputs.firstName}
              onChangeText={(text) => handleOnChange(text, "firstName")}
              error={errors.firstName}
            />
            <Input
              label="Last Name"
              iconName="id-badge"
              required
              value={inputs.lastName}
              onChangeText={(text) => handleOnChange(text, "lastName")}
              error={errors.lastName}
            />
            <Input
              label="Date of birth"
              iconName="calendar"
              required
              value={inputs.dateOfBirth}
              onChangeText={(text) => handleOnChange(text, "dateOfBirth")}
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
              onChangeText={(text) => handleOnChange(text, "bio")}
              error={errors.bio}
            />

            <InputLabel label="Currently I'm..." required />
            <ButtonsWSContainer>
              <FilterButton
                title="Study"
                onPress={() => {
                  setActive({ study: true, work: false, nothing: false });
                  setIsStudying(true);
                  setIsWorking(false);
                }}
                color="dimgray"
                active={active.study}
              />
              <FilterButton
                title="Work"
                onPress={() => {
                  setActive({ study: false, work: true, nothing: false });
                  setIsStudying(false);
                  setIsWorking(true);
                }}
                color="dimgray"
                active={active.work}
              />
              <FilterButton
                title="Nothing"
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
                onChangeText={(text) => handleOnChange(text, "currentJobRole")}
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
                  onChangeText={(text) => handleOnChange(text, "university")}
                  error={errors.university}
                />
                <Input
                  label="Degree"
                  iconName="book"
                  required
                  value={inputs.degree}
                  onChangeText={(text) => handleOnChange(text, "degree")}
                  error={errors.degree}
                />
                <Input
                  label="Graduation year"
                  iconName="graduation-cap"
                  required
                  value={inputs.graduationYear}
                  onChangeText={(text) =>
                    handleOnChange(text, "graduationYear")
                  }
                  placeholder="DD/MM/YYYY"
                  placeholderTextColor="#969696"
                  error={errors.graduationYear}
                />
              </>
            )}

            <ButtonContainer>
              <Button
                title="Register"
                onPress={validate}
                color="#58a659"
                iconName="check-square-o"
              />
            </ButtonContainer>
          </>
        )}
        <Toast />
      </ScrollView>
    </Container>
  );
}
