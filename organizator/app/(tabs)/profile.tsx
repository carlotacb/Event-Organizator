import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  SafeAreaView,
  ScrollView,
  Text,
  View,
} from "react-native";
import { router } from "expo-router";
import styled from "styled-components/native";
import Toast from "react-native-toast-message";
import {
  getMyInformation,
  updateMyInformation,
} from "../../utils/api/axiosUsers";
import { getToken } from "../../utils/sessionCalls";
import { UserInformation } from "../../utils/interfaces/Users";
import Input from "../../components/Input";
import Button from "../../components/StyledButton";

const Container = styled(SafeAreaView)`
  padding: 30px;
  background-color: white;
  flex: 1;
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
      const token = await getToken();
      if (token === null) {
        router.replace("/login");
      }

      return getMyInformation(token);
    };

    fetchData()
      .then((response) => {
        setLoading(false);
        setUserInformation(response.userInformation);
        setInputs({
          firstName: response.userInformation?.firstName || "",
          lastName: response.userInformation?.lastName || "",
          bio: response.userInformation?.bio || "",
        });
      })
      .catch((error) => console.log(error));
  }, []);

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
            <Title>Hi, {userInformation?.username} 👋🏼</Title>
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
                <Button title="Edit information" onPress={editProfile} />
              </ButtonContainer>
            </InputsContainer>
          </>
        )}
        <Toast />
      </ScrollView>
    </Container>
  );
}
