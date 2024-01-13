import React, { useEffect, useState } from "react";
// @ts-ignore
import styled from "styled-components/native";
import { SafeAreaView, Text, ScrollView, View, Pressable } from "react-native";

import { Link, router } from "expo-router";
import Toast from "react-native-toast-message";
import Button from "../components/componentsStyled/Buttons/ButtonWithIcon";
import { loginUser } from "../utils/api/axiosUsers";
import { LoginResponse } from "../utils/interfaces/Users";
import { getToken, storeToken } from "../utils/sessionCalls";
import {
  SubTitle,
  Title,
} from "../components/componentsStyled/Shared/TextStyles";
import { systemColors } from "../components/componentsStyled/tokens";
import { MaxWidthUseScreen } from "../components/componentsStyled/Shared/ContainerStyles";
import LoginForm from "../components/componentsStyled/Forms/LoginForm";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

const RegisterTextContainer = styled(View)`
  display: flex;
  flex-direction: row;
  gap: 5px;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 50px;
`;

const RegisterText = styled(Text)`
  text-align: center;
  font-size: 15px;
`;

const RegisterButton = styled(Text)`
  font-weight: bold;
  font-size: 15px;
  color: #6161e0;
`;

export default function LoginPage() {
  const [loading, setLoading] = React.useState(false);
  const [inputs, setInputs] = useState({
    username: "",
    password: "",
  });

  useEffect(() => {
    getToken().then((token) => {
      if (token) {
        router.replace("/");
      }
    });
  });

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

  return (
    <Container>
      <ScrollView
        contentContainerStyle={{
          padding: 60,
          flexGrow: 1,
          justifyContent: "center",
        }}
      >
        <Toast />
        {loading ? (
          <LoginPage />
        ) : (
          <MaxWidthUseScreen>
            <Title>Welcome back!</Title>
            <SubTitle>Please enter your credentials to log in.</SubTitle>
            <LoginForm login={login} inputs={inputs} setInputs={setInputs} />
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
                <Button
                  title="Go to homepage"
                  onPress={() => {}}
                  iconName="home"
                  color={systemColors.action}
                  fontSize="14px"
                />
              </Link>
            </RegisterTextContainer>
          </MaxWidthUseScreen>
        )}
      </ScrollView>
    </Container>
  );
}
