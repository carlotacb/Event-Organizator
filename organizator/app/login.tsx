import React, { useEffect, useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import { SafeAreaView, Text, ScrollView, View, Pressable } from "react-native";

import { Link, router } from "expo-router";
import Toast from "react-native-toast-message";
import Input from "../components/Input";
import Button from "../components/ButtonWithIcon";
import { loginUser } from "../utils/api/axiosUsers";
import { LoginResponse } from "../utils/interfaces/Users";
import { getToken, storeToken } from "../utils/sessionCalls";
import FilterButton from "../components/FilterButtons";

const Container = styled(SafeAreaView)`
  padding: 50px 40px;
  background-color: white;
  flex: 1;
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

const RegisterTextContainer = styled(View)`
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  justify-content: center;
  margin-top: 40px;
`;

const RegisterText = styled(Text)`
  text-align: center;
  font-size: 15px;
`;

const RegisterButton = styled(Text)`
  font-weight: bold;
  text-decoration: underline #6161e0;
  font-size: 18px;
  color: #6161e0;
`;

export default function LoginPage() {
  const [inputs, setInputs] = useState({
    username: "",
    password: "",
  });
  const [errors, setErrors] = React.useState({
    username: undefined,
    password: undefined,
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
    let isValid = true;

    if (!inputs.username) {
      handleError("Please enter your username", "username");
      isValid = false;
    } else {
      handleError(undefined, "username");
    }

    if (!inputs.password) {
      handleError("Please enter a password", "password");
      isValid = false;
    } else {
      handleError(undefined, "password");
    }

    if (isValid) {
      login();
    }
  };

  const login = () => {
    setLoading(true);
    loginUser(inputs).then((response: LoginResponse) => {
      setLoading(false);
      if (response.error) {
        Toast.show({
          type: "error",
          text1: "Error",
          text2: response.error,
        });
      } else {
        storeToken(response.token);
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
      <ScrollView
        contentContainerStyle={{
          padding: 20,
          flex: 1,
          justifyContent: "center",
        }}
      >
        <Toast />
        {loading ? (
          <LoginPage />
        ) : (
          <>
            <Title>Welcome back!</Title>
            <SubTitle>Please enter your credentials to log in.</SubTitle>
            <Input
              label="Username"
              iconName="user"
              value={inputs.username}
              required
              onChangeText={(text) => handleOnChange(text, "username")}
              error={errors.username}
            />
            <Input
              label="Password"
              iconName="lock"
              value={inputs.password}
              required
              onChangeText={(text) => handleOnChange(text, "password")}
              error={errors.password}
              password
            />
            <ButtonContainer>
              <Button
                title="Log in"
                onPress={validate}
                iconName="sign-in"
                color="#58a659"
              />
            </ButtonContainer>
            <RegisterTextContainer>
              <RegisterText>You don't have an account yet? </RegisterText>
              <Link href="/register" asChild>
                <Pressable>
                  <RegisterButton>Register now</RegisterButton>
                </Pressable>
              </Link>
            </RegisterTextContainer>
            <RegisterTextContainer>
              <Link href="/" asChild>
                <FilterButton
                  title="Go to homepage"
                  onPress={() => {}}
                  iconName="home"
                  color="#040240"
                  active
                />
              </Link>
            </RegisterTextContainer>
          </>
        )}
      </ScrollView>
    </Container>
  );
}
