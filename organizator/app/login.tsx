import React, { useEffect, useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import {
  SafeAreaView,
  Text,
  ScrollView,
  ActivityIndicator,
  View,
  Pressable,
} from "react-native";

import { Link, router } from "expo-router";
import Toast from "react-native-toast-message";
import Input from "../components/Input";
import Button from "../components/StyledButton";
import { loginUser } from "../utils/api/axiosUsers";
import { LoginResponse } from "../utils/interfaces/Users";
import { getToken, storeToken } from "../utils/sessionCalls";

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

const RegisterText = styled(Text)`
  text-align: center;
  margin-top: 10px;
  font-size: 15px;
`;

const RegisterButton = styled(Pressable)`
  font-weight: bold;
  color: #36368a;
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
        router.replace("/home");
      }
    });
  });

  const validate = () => {
    let isValid = false;

    if (!inputs.username) {
      handleError("Please enter your username", "username");
      isValid = false;
    } else {
      handleError(undefined, "username");
      isValid = true;
    }

    if (!inputs.password) {
      handleError("Please enter a password", "password");
      isValid = false;
    } else {
      handleError(undefined, "password");
      isValid = true;
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
          text1: "There is an error!!",
          text2: response.error,
        });
      } else {
        storeToken(response.token);
        router.replace("/home");
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
          <View style={{ flex: 1, justifyContent: "center" }}>
            <ActivityIndicator size="large" />
          </View>
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
              <Button title="Log in" onPress={validate} />
            </ButtonContainer>
            <RegisterText>
              You don't have an account yet?{" "}
              <Link href="/register" asChild>
                <RegisterButton>
                  <Text>Register now</Text>
                </RegisterButton>
              </Link>
            </RegisterText>
          </>
        )}
      </ScrollView>
    </Container>
  );
}
