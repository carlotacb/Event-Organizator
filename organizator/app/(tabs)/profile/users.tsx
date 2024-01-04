import React, { useEffect, useState } from "react";
import { View, Text, ScrollView, SafeAreaView, Pressable } from "react-native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
// @ts-ignore
import styled from "styled-components/native";
import Toast from "react-native-toast-message";
import { Dialog } from "react-native-simple-dialogs";
import { router } from "expo-router";
import {
  getAllUsersRoles,
  getUserRole,
  updateRoleForUser,
} from "../../../utils/api/axiosUsers";
import {
  UserRoleInformation,
  UserRoles,
} from "../../../utils/interfaces/Users";
import LoadingPage from "../../../components/LodingPage";
import Button from "../../../components/ButtonWithIcon";
import { getToken } from "../../../utils/sessionCalls";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

const UserLine = styled(View)`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  border-bottom-width: 1px;
  border-bottom-color: #e6e6e6;
`;

const Username = styled(Text)`
  font-weight: bold;
  font-size: 15px;
`;

const ButtonAndRole = styled(View)`
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: center;
`;

export default function AllUsers() {
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState<UserRoleInformation[] | null>(null);
  const [alertVisible, setAlertVisible] = useState(false);
  const [idToUpdate, setIdToUpdate] = useState<string | null>(null);
  const [trigger, setTrigger] = useState(false);

  useEffect(() => {
    // @ts-ignore
    const fetchData = async () => getAllUsersRoles();

    fetchData().then((response) => {
      setLoading(false);
      setUsers(response.users || null);
    });
  }, [trigger]);

  const updateRole = (role: string) => {
    const fetchData = async () => {
      const token = await getToken();
      return updateRoleForUser(idToUpdate || "", token || "", role);
    };

    fetchData()
      .then((response) => {
        Toast.show({
          type: "success",
          text1: "Role updated",
          text2: `The user ${response.user?.username} has been updated to ${role}`,
          visibilityTime: 3000,
          autoHide: true,
        });
        setAlertVisible(false);
        setIdToUpdate(null);
        setTrigger(!trigger);
      })
      .catch((error) => {
        setAlertVisible(false);
        setIdToUpdate(null);
        Toast.show({
          type: "error",
          text1: "Error",
          text2: `The user has not been updated because ${error}`,
          visibilityTime: 3000,
          autoHide: true,
        });
      });
  };

  return (
    <Container>
      <ScrollView contentContainerStyle={{ padding: 25 }}>
        {loading ? (
          <LoadingPage />
        ) : (
          <>
            {users?.map((user) => (
              <UserLine key={user.id}>
                <Username>{user.username}</Username>
                <ButtonAndRole>
                  <Text>{user.role}</Text>
                  <Pressable
                    onPress={() => {
                      setAlertVisible(true);
                      setIdToUpdate(user.id);
                    }}
                  >
                    <FontAwesome name="edit" size={18} />
                  </Pressable>
                </ButtonAndRole>
              </UserLine>
            ))}
          </>
        )}

        <Dialog
          visible={alertVisible}
          title="Which role do you want to give?"
          onTouchOutside={() => {
            setAlertVisible(false);
            setIdToUpdate(null);
          }}
          onRequestClose={() => {
            setAlertVisible(false);
            setIdToUpdate(null);
          }}
          contentInsetAdjustmentBehavior="automatic"
        >
          <View>
            <Button
              title="Participant"
              iconName="user"
              onPress={() => {
                updateRole("PARTICIPANT");
              }}
              color="#040240"
            />
            <Button
              title="Organizer"
              iconName="user-secret"
              onPress={() => {
                updateRole("ORGANIZER");
              }}
              color="#040240"
            />
            <Button
              title="Admin"
              iconName="star"
              onPress={() => {
                updateRole("ORGANIZER_ADMIN");
              }}
              color="#040240"
            />
          </View>
        </Dialog>
      </ScrollView>
      <Toast />
    </Container>
  );
}
