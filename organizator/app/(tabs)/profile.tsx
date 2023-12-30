import React, { useEffect, useState } from "react";
import { Pressable, SafeAreaView, ScrollView, Text, View } from "react-native";
import { router } from "expo-router";
// @ts-ignore
import styled from "styled-components/native";
import Toast from "react-native-toast-message";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import {
  getMyInformation,
  logout,
  updateMyInformation,
} from "../../utils/api/axiosUsers";
import { getToken, removeToken } from "../../utils/sessionCalls";
import { UserInformation } from "../../utils/interfaces/Users";
import Input from "../../components/Input";
import Button from "../../components/StyledButton";
import LoadingPage from "../../components/LodingPage";

const Container = styled(SafeAreaView)`
  padding: 30px;
  background-color: white;
  flex: 1;
`;

const TitleContainer = styled(View)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
`;

const Title = styled(Text)`
  font-size: 30px;
  font-weight: bold;
  color: black;
`;

const InputsContainer = styled(View)`
  margin-top: 30px;
`;

const ButtonContainer = styled(View)`
  display: flex;
  margin-top: 15px;
  align-items: center;
`;

export default function Profile() {
  const [loading, setLoading] = React.useState(true);
  const [token, setToken] = React.useState<string | null>(null);
  const [userInformation, setUserInformation] =
    React.useState<UserInformation | null>(null);
  const [inputs, setInputs] = useState({
    firstName: userInformation?.firstName || "",
    lastName: userInformation?.lastName || "",
    bio: userInformation?.bio || "",
  });
  const [errors, setErrors] = React.useState({
    firstName: undefined,
    lastName: undefined,
    bio: undefined,
  });

  useEffect(() => {
    const fetchData = async () => {
      const t = await getToken();
      if (t === null) {
        router.replace("/login");
      }

      setToken(t);
      return getMyInformation(t);
    };

    fetchData().then((response) => {
      setLoading(false);
      setUserInformation(response.userInformation);
      setInputs({
        firstName: response.userInformation?.firstName || "",
        lastName: response.userInformation?.lastName || "",
        bio: response.userInformation?.bio || "",
      });
    });
  }, []);

  const validate = () => {
    let isValid = false;

    if (inputs.firstName === "") {
      handleError("First name is required", "firstName");
    } else {
      handleError(undefined, "firstName");
    }

    if (inputs.lastName === "") {
      handleError("Last name is required", "lastName");
    } else {
      handleError(undefined, "lastName");
    }

    if (inputs.bio === "") {
      handleError("Biography is required", "bio");
    } else {
      handleError(undefined, "bio");
    }

    if (
      errors.firstName === undefined &&
      errors.lastName === undefined &&
      errors.bio === undefined
    ) {
      isValid = true;
    }

    if (isValid) editProfile();
  };

  const editProfile = () => {
    setLoading(true);
    updateMyInformation(inputs, userInformation?.id || "").then((response) => {
      if (response.error) {
        setLoading(false);
        Toast.show({
          type: "error",
          text1: "Error",
          text2: response.error,
          visibilityTime: 8000,
        });
      } else {
        setLoading(false);
      }
    });
  };

  const loggingOut = () => {
    logout(token);
    removeToken();
    router.replace("/login");
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
          <LoadingPage />
        ) : (
          <>
            <TitleContainer>
              <Title>Hi, {userInformation?.username} 👋🏼</Title>
              <Pressable onPress={loggingOut}>
                <FontAwesome name="sign-out" size={30} color="red" />
              </Pressable>
            </TitleContainer>
            <InputsContainer>
              <Input
                label="Email"
                iconName="at"
                value={userInformation?.email}
                disabled
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
                <Button title="Edit information" onPress={validate} />
              </ButtonContainer>
            </InputsContainer>
          </>
        )}
        <Toast />
      </ScrollView>
    </Container>
  );
}
