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
  updateRoleForUser,
} from "../../../utils/api/axiosUsers";
import { UserRoleInformation } from "../../../utils/interfaces/Users";
import LoadingPage from "../../../components/LodingPage";
import Button from "../../../components/ButtonWithIcon";
import { getToken, removeToken } from "../../../utils/sessionCalls";
import FilterButton from "../../../components/FilterButtons";

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

const ButtonsContainer = styled(View)`
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  gap: 5px;
  margin-bottom: 20px;
`;

export default function AllUsers() {
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState<UserRoleInformation[] | null>(null);
  const [alertVisible, setAlertVisible] = useState(false);
  const [idToUpdate, setIdToUpdate] = useState<string | null>(null);
  const [userToUpdate, setUserToUpdate] = useState<string | null>(null);
  const [trigger, setTrigger] = useState(false);
  const [allUsers, setAllUsers] = useState<UserRoleInformation[] | null>(null);
  const [active, setActive] = useState({
    all: true,
    organizerAdmin: false,
    organizer: false,
    participant: false,
  });

  useEffect(() => {
    // @ts-ignore
    const fetchData = async () => getAllUsersRoles();

    fetchData().then((response) => {
      setLoading(false);
      setUsers(response.users || null);
      setAllUsers(response.users || null);
    });
  }, [trigger]);

  const updateRole = (role: string) => {
    const fetchData = async () => {
      const token = await getToken();
      return updateRoleForUser(idToUpdate || "", token || "", role);
    };

    fetchData().then((response) => {
      if (response.error) {
        if (response.error === "Only authorized to organizer admin") {
          router.back();
        }
        if (
          response.error === "Unauthorized" ||
          response.error === "Invalid token" ||
          response.error === "User does not exist"
        ) {
          removeToken();
          router.replace("/login");
        }
        setAlertVisible(false);
        setIdToUpdate(null);
        Toast.show({
          type: "error",
          text1: "Error",
          text2: `The user has not been updated because ${response.error}`,
          visibilityTime: 3000,
          autoHide: true,
        });
      }
      Toast.show({
        type: "success",
        text1: "Role updated",
        text2: `The user ${response.user?.username} has been updated to ${role}`,
        visibilityTime: 3000,
        autoHide: true,
      });
      setAlertVisible(false);
      setIdToUpdate(null);
      setActive(() => ({
        all: true,
        organizerAdmin: false,
        organizer: false,
        participant: false,
      }));
      setTrigger(!trigger);
    });
  };

  return (
    <Container>
      <ScrollView contentContainerStyle={{ padding: 25 }}>
        {loading ? (
          <LoadingPage />
        ) : (
          <View>
            <ButtonsContainer>
              <FilterButton
                title="All"
                onPress={() => {
                  setUsers(allUsers);
                  setActive(() => ({
                    all: true,
                    organizerAdmin: false,
                    organizer: false,
                    participant: false,
                  }));
                }}
                color="#040240"
                iconName="list"
                active={active.all}
              />
              <FilterButton
                title=""
                onPress={() => {
                  setUsers(
                    allUsers?.filter(
                      (user) => user.role === "Organizer admin",
                    ) || [],
                  );

                  setActive(() => ({
                    all: false,
                    organizerAdmin: true,
                    organizer: false,
                    participant: false,
                  }));
                }}
                color="#040240"
                iconName="star"
                active={active.organizerAdmin}
              />
              <FilterButton
                title=""
                onPress={() => {
                  setUsers(
                    allUsers?.filter((user) => user.role === "Organizer") || [],
                  );
                  setActive(() => ({
                    all: false,
                    organizerAdmin: false,
                    organizer: true,
                    participant: false,
                  }));
                }}
                color="#040240"
                iconName="user-secret"
                active={active.organizer}
              />
              <FilterButton
                title=""
                onPress={() => {
                  setUsers(
                    allUsers?.filter((user) => user.role === "Participant") ||
                      [],
                  );
                  setActive(() => ({
                    all: false,
                    organizerAdmin: false,
                    organizer: false,
                    participant: true,
                  }));
                }}
                color="#040240"
                iconName="user"
                active={active.participant}
              />
            </ButtonsContainer>
            {users?.map((user) => (
              <UserLine key={user.id}>
                <Username>{user.username}</Username>
                <ButtonAndRole>
                  <Text>{user.role}</Text>
                  <Pressable
                    onPress={() => {
                      setAlertVisible(true);
                      setIdToUpdate(user.id);
                      setUserToUpdate(user.username);
                    }}
                  >
                    <FontAwesome name="edit" size={18} />
                  </Pressable>
                </ButtonAndRole>
              </UserLine>
            ))}
          </View>
        )}

        <Dialog
          visible={alertVisible}
          title={`Which role do you want to give to ${userToUpdate}?`}
          onTouchOutside={() => {
            setAlertVisible(false);
            setIdToUpdate(null);
            setUserToUpdate(null);
          }}
          onRequestClose={() => {
            setAlertVisible(false);
            setIdToUpdate(null);
            setUserToUpdate(null);
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
