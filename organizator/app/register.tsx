import React, { useEffect, useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import {
  SafeAreaView,
  Text,
  ScrollView,
  ActivityIndicator,
  View,
} from "react-native";

import { router } from "expo-router";
import Toast from "react-native-toast-message";
import Input from "../components/Input";
import Button from "../components/StyledButton";
import { registerUser } from "../utils/api/axiosUsers";
import { RegisterResponse } from "../utils/interfaces/Users";
import { getToken } from "../utils/sessionCalls";

const Container = styled(SafeAreaView)`
  padding: 50px 40px;
  background-color: white;
`;

const Title = styled(Text)`
  font-size: 40px;
  font-weight: bold;
  color: black;
  text-align: center;
`;

const SubTitle = styled(Text)`
  font-size: 18px;
  color: gray;
  margin: 5px 0 20px 0;
  text-align: center;
`;

const ButtonContainer = styled(View)`
  display: flex;
  margin-top: 15px;
  align-items: center;
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
  });
  const [errors, setErrors] = React.useState({
    username: undefined,
    email: undefined,
    password: undefined,
    passwordConfirm: undefined,
    firstName: undefined,
    lastName: undefined,
    bio: undefined,
  });
  const [loading, setLoading] = React.useState(false);

  useEffect(() => {
    getToken().then((token) => {
      if (token) {
        router.replace("/");
      }
    });
  });

  const validate = () => {
    let isValid = false;

    if (!inputs.username) {
      handleError("Please enter your username", "username");
    } else {
      handleError(undefined, "username");
    }

    if (!inputs.email) {
      handleError("Please enter an email address", "email");
    } else if (!inputs.email.match(/\S+@\S+\.\S+/)) {
      handleError("Please enter a valid email address", "email");
    } else {
      handleError(undefined, "email");
    }

    if (!inputs.password) {
      handleError("Please enter a password", "password");
    } else if (inputs.password.length < 8) {
      handleError("Minimum password length is 8", "password");
    } else {
      handleError(undefined, "password");
    }

    if (!inputs.passwordConfirm) {
      handleError("Please enter confirm password", "passwordConfirm");
    } else if (inputs.passwordConfirm !== inputs.password) {
      handleError("Password confirmation does not match", "passwordConfirm");
    } else {
      handleError(undefined, "passwordConfirm");
    }

    if (!inputs.firstName) {
      handleError("Please enter your first name", "firstName");
    } else {
      handleError(undefined, "firstName");
    }

    if (!inputs.lastName) {
      handleError("Please enter your last name", "lastName");
    } else {
      handleError(undefined, "lastName");
    }

    if (!inputs.bio) {
      handleError("Please enter your bio", "bio");
    } else {
      handleError(undefined, "bio");
    }

    if (
      errors.username === undefined &&
      errors.email === undefined &&
      errors.password === undefined &&
      errors.passwordConfirm === undefined &&
      errors.firstName === undefined &&
      errors.lastName === undefined &&
      errors.bio === undefined
    ) {
      isValid = true;
    }

    if (isValid) {
      register();
    }
  };

  const register = () => {
    setLoading(true);
    registerUser(inputs).then((response: RegisterResponse) => {
      setLoading(false);
      if (response.error) {
        Toast.show({
          type: "error",
          text1: "Error",
          text2: response.error,
          visibilityTime: 8000,
        });
      } else {
        router.replace("/(home)login");
      }
    });
  };

  const handleOnChange = (text: string, input: string) => {
    setInputs((prevState) => ({ ...prevState, [input]: text }));
  };
  const handleError = (text: string | undefined, input: string) => {
    setErrors((prevState) => ({ ...prevState, [input]: text }));
  };

  return (
    <Container>
      <ScrollView contentContainerStyle={{ padding: 20 }}>
        {loading ? (
          <View style={{ flex: 1, justifyContent: "center" }}>
            <ActivityIndicator size="large" />
          </View>
        ) : (
          <>
            <Title>Welcome!</Title>
            <SubTitle>
              We are happy to have you here! Please fill in the following
              details
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
              label="Biography"
              iconName="pencil"
              required
              value={inputs.bio}
              onChangeText={(text) => handleOnChange(text, "bio")}
              error={errors.bio}
            />

            <ButtonContainer>
              <Button title="Register" onPress={validate} />
            </ButtonContainer>
          </>
        )}
        <Toast />
      </ScrollView>
    </Container>
  );
}
