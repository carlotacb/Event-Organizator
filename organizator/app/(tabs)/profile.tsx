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
import { UserInformation, UserRoles } from "../../utils/interfaces/Users";
import Input from "../../components/Input";
import Button from "../../components/StyledButton";
import LoadingPage from "../../components/LodingPage";

const Container = styled(SafeAreaView)`
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

const TagsContainer = styled(View)`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 10px;
`;

const ButtonContainer = styled(View)`
  display: flex;
  margin-top: 20px;
  align-items: center;
`;

const Tag = styled(View)<{ backgroundColor: string }>`
  background-color: ${(props: { backgroundColor: string }) =>
    props.backgroundColor};
  border: 2px solid #233277;
  border-radius: 50%;
  padding: 5px 15px;
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 5px;
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

  const parseRole = (role: string): string => {
    switch (role) {
      case UserRoles.ORGANIZER_ADMIN:
        return "ADMIN";
      case UserRoles.ORGANIZER:
        return "Organizer";
      default:
        return "User";
    }
  };

  const getBackGroundColorForRole = (role: string): string => {
    switch (role) {
      case UserRoles.ORGANIZER_ADMIN:
        return "#cea6aa";
      case UserRoles.ORGANIZER:
        return "#aba6ce";
      default:
        return "#a6cea6";
    }
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
            <TagsContainer>
              <Tag
                backgroundColor={getBackGroundColorForRole(
                  userInformation?.role || "",
                )}
              >
                <Text>{parseRole(userInformation?.role || "")}</Text>
              </Tag>
              <Tag backgroundColor="transparent">
                <FontAwesome name="at" size={15} color="#233277" />
                <Text>{userInformation?.email}</Text>
              </Tag>
            </TagsContainer>
            <InputsContainer>
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
