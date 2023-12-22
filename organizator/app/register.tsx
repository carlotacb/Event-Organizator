import React, { useState } from "react";
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
import registerUser from "../utils/api/axiosUsers";
import { RegisterResponse } from "../utils/interfaces/Users";

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
    // profilePicture: "",
  });
  const [errors, setErrors] = React.useState({
    username: undefined,
    email: undefined,
    password: undefined,
    passwordConfirm: undefined,
    firstName: undefined,
    lastName: undefined,
    bio: undefined,
    // profilePicture: undefined,
  });
  const [loading, setLoading] = React.useState(false);

  const validate = () => {
    let isValid = false;

    if (!inputs.username) {
      handleError("Please enter your username", "username");
      isValid = false;
    } else {
      handleError(undefined, "username");
      isValid = true;
    }

    if (!inputs.email) {
      handleError("Please enter an email address", "email");
      isValid = false;
    } else if (!inputs.email.match(/\S+@\S+\.\S+/)) {
      handleError("Please enter a valid email address", "email");
      isValid = false;
    } else {
      handleError(undefined, "email");
      isValid = true;
    }

    if (!inputs.password) {
      handleError("Please enter a password", "password");
      isValid = false;
    } else if (inputs.password.length < 8) {
      handleError("Minimum password length is 8", "password");
      isValid = false;
    } else {
      handleError(undefined, "password");
      isValid = true;
    }

    if (!inputs.passwordConfirm) {
      handleError("Please enter confirm password", "passwordConfirm");
      isValid = false;
    } else if (inputs.passwordConfirm !== inputs.password) {
      handleError("Password confirmation does not match", "passwordConfirm");
      isValid = false;
    } else {
      handleError(undefined, "passwordConfirm");
      isValid = true;
    }

    if (!inputs.firstName) {
      handleError("Please enter your first name", "firstName");
      isValid = false;
    } else {
      handleError(undefined, "firstName");
      isValid = true;
    }

    if (!inputs.lastName) {
      handleError("Please enter your last name", "lastName");
      isValid = false;
    } else {
      handleError(undefined, "lastName");
      isValid = true;
    }

    if (!inputs.bio) {
      handleError("Please enter your bio", "bio");
      isValid = false;
    } else {
      handleError(undefined, "bio");
      isValid = true;
    }

    /* if (!inputs.profilePicture) {
      handleError("Please enter your profile picture", "profilePicture");
      isValid = false;
    } else {
      handleError(undefined, "profilePicture");
      isValid = true;
    } */

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
        });
      } else {
        Toast.show({
          type: "success",
          text1: "Congratulations!",
          text2: "You are now part of the community!",
          position: "top",
          visibilityTime: 4000,
          autoHide: true,
          topOffset: 40,
        });
        router.replace("/");
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
      {loading ? (
        <View style={{ flex: 1, justifyContent: "center" }}>
          <ActivityIndicator size="large" />
        </View>
      ) : (
        <ScrollView contentContainerStyle={{ padding: 20 }}>
          <Toast />
          <Title>Welcome!</Title>
          <SubTitle>
            We are happy to have you here! Please fill in the following details
          </SubTitle>
          <Input
            label="Username"
            iconName="user"
            required
            onChangeText={(text) => handleOnChange(text, "username")}
            error={errors.username}
          />
          <Input
            label="Email"
            iconName="at"
            required
            onChangeText={(text) => handleOnChange(text, "email")}
            error={errors.email}
            keyboardType="email-address"
          />
          <Input
            label="Password"
            iconName="lock"
            required
            onChangeText={(text) => handleOnChange(text, "password")}
            error={errors.password}
            password
          />
          <Input
            label="Confirm your password"
            required
            iconName="lock"
            onChangeText={(text) => handleOnChange(text, "passwordConfirm")}
            error={errors.passwordConfirm}
            password
          />
          <Input
            label="First Name"
            iconName="id-badge"
            required
            onChangeText={(text) => handleOnChange(text, "firstName")}
            error={errors.firstName}
          />
          <Input
            label="Last Name"
            iconName="id-badge"
            required
            onChangeText={(text) => handleOnChange(text, "lastName")}
            error={errors.lastName}
          />
          <Input
            label="Biography"
            iconName="pencil"
            required
            onChangeText={(text) => handleOnChange(text, "bio")}
            error={errors.bio}
          />
          {/* <Input
            label="Profile Picture"
            iconName="camera"
            required
            onChangeText={(text) => handleOnChange(text, "profilePicture")}
            error={errors.profilePicture}
          /> */}

          <ButtonContainer>
            <Button title="Register" onPress={validate} />
          </ButtonContainer>
        </ScrollView>
      )}
    </Container>
  );
}
