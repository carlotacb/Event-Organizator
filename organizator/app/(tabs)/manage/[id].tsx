import React, { useEffect, useState } from "react";
import { Pressable, SafeAreaView, ScrollView, Text, View } from "react-native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
// @ts-ignore
import styled from "styled-components/native";
import Toast from "react-native-toast-message";
import { router, useLocalSearchParams } from "expo-router";
import { Dialog } from "react-native-simple-dialogs";
import LoadingPage from "../../../components/LodingPage";
import { getToken, removeToken } from "../../../utils/sessionCalls";
import {
  getParticipants,
  updateApplicationStatus,
} from "../../../utils/api/axiosApplications";
import { ParticipantsInformation } from "../../../utils/interfaces/Applications";
import EmptyPage from "../../../components/EmptyPage";
import FilterButton from "../../../components/FilterButtons";
import Button from "../../../components/ButtonWithIcon";
import { getUserRole } from "../../../utils/api/axiosUsers";
import { UserRoles } from "../../../utils/interfaces/Users";

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
  font-size: 15px;
`;

const ButtonAndRole = styled(View)`
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: center;
`;

const TagStatus = styled(View)<{ backgroundColor: string }>`
  border: 2px solid
    ${(props: { backgroundColor: string }) => props.backgroundColor};
  background-color: ${(props: { backgroundColor: string }) =>
    props.backgroundColor};
  padding: 5px 10px;
  border-radius: 20px;
  color: white;
`;

const ButtonsContainer = styled(View)`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 5px;
  margin-bottom: 20px;
`;

const ParticipantsNumber = styled(Text)`
  text-align: right;
  font-size: 16px;
  margin-bottom: 20px;
  margin-right: 20px;
  font-style: italic;
  color: dimgray;
`;

export default function Id() {
  const { id } = useLocalSearchParams();
  const [loading, setLoading] = useState(true);
  const [userToUpdate, setUserToUpdate] = useState<string | null>(null);
  const [idToUpdate, setIdToUpdate] = useState<string | null>(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [applications, setApplications] = useState<
    ParticipantsInformation[] | null
  >(null);
  const [alertVisible, setAlertVisible] = useState(false);
  const [allApplications, setAllApplications] = useState<
    ParticipantsInformation[] | null
  >(null);
  const [trigger, setTrigger] = useState(false);
  const [stats, setStats] = useState({
    all: 0,
    confirmed: 0,
    rejected: 0,
    underReview: 0,
    invited: 0,
    cancelled: 0,
    invalid: 0,
    waitList: 0,
  });
  const [active, setActive] = useState({
    all: true,
    confirmed: false,
    rejected: false,
    underReview: false,
    invited: false,
    cancelled: false,
    invalid: false,
    waitList: false,
  });

  useEffect(() => {
    const fetchData = async () => {
      const token = await getToken();
      // @ts-ignore
      return getParticipants(token || "", id);
    };
    const fetchAdminFunction = async () => {
      const t = await getToken();
      return getUserRole(t);
    };

    fetchData().then((response) => {
      setLoading(false);
      setAllApplications(response.participants || []);
      setApplications(response.participants || []);

      setStats({
        all: response.participants?.length || 0,
        confirmed:
          response.participants?.filter(
            (participant) => participant.status === "Confirmed",
          ).length || 0,
        rejected:
          response.participants?.filter(
            (participant) => participant.status === "Rejected",
          ).length || 0,
        underReview:
          response.participants?.filter(
            (participant) => participant.status === "Under review",
          ).length || 0,
        invited:
          response.participants?.filter(
            (participant) => participant.status === "Invited",
          ).length || 0,
        cancelled:
          response.participants?.filter(
            (participant) => participant.status === "Cancelled",
          ).length || 0,
        invalid:
          response.participants?.filter(
            (participant) => participant.status === "Invalid",
          ).length || 0,
        waitList:
          response.participants?.filter(
            (participant) => participant.status === "Wait list",
          ).length || 0,
      });
    });
    fetchAdminFunction().then((response) => {
      setIsAdmin(response.role === UserRoles.ORGANIZER_ADMIN);
    });
  }, [trigger]);

  const updateStatus = (status: string) => {
    const fetchData = async () => {
      const token = await getToken();
      return updateApplicationStatus(token || "", idToUpdate || "", status);
    };

    fetchData().then((response) => {
      if (response.error) {
        if (
          response.error === "Unauthorized" ||
          response.error === "Invalid token" ||
          response.error === "User does not exist"
        ) {
          removeToken();
          router.replace("/login");
        } else {
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
      } else {
        Toast.show({
          type: "success",
          text1: "Role updated",
          text2: `The user ${userToUpdate} is now ${status}`,
          visibilityTime: 3000,
          autoHide: true,
        });
        setAlertVisible(false);
        setIdToUpdate(null);
        setUserToUpdate(null);
        setActive(() => ({
          all: true,
          confirmed: false,
          rejected: false,
          underReview: false,
          invited: false,
          cancelled: false,
          invalid: false,
          waitList: false,
        }));
        setTrigger(!trigger);
      }
    });
  };

  const getTagColor = (status: string): string => {
    if (status === "Under review") return "#f8d280";
    if (status === "Invited") return "#74b3fc";
    if (status === "Rejected") return "#ff7f7f";
    if (status === "Cancelled") return "#d33737";
    if (status === "Confirmed") return "#6cd27b";
    if (status === "Invalid") return "#867f7f";
    if (status === "Wait list") return "#b694f5";

    return "#000000";
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
                title={`All (${stats.all})`}
                onPress={() => {
                  setApplications(allApplications);
                  setActive(() => ({
                    all: true,
                    confirmed: false,
                    rejected: false,
                    underReview: false,
                    invited: false,
                    cancelled: false,
                    invalid: false,
                    waitList: false,
                  }));
                }}
                color="#040240"
                active={active.all}
              />
              <FilterButton
                title={`Under Review (${stats.underReview})`}
                onPress={() => {
                  setApplications(
                    allApplications?.filter(
                      (participant) => participant.status === "Under review",
                    ) || [],
                  );
                  setActive(() => ({
                    all: false,
                    confirmed: false,
                    rejected: false,
                    underReview: true,
                    invited: false,
                    cancelled: false,
                    invalid: false,
                    waitList: false,
                  }));
                }}
                color={getTagColor("Under review")}
                active={active.underReview}
              />
              <FilterButton
                title={`Invited (${stats.invited})`}
                onPress={() => {
                  setApplications(
                    allApplications?.filter(
                      (participant) => participant.status === "Invited",
                    ) || [],
                  );
                  setActive(() => ({
                    all: false,
                    confirmed: false,
                    rejected: false,
                    underReview: false,
                    invited: true,
                    cancelled: false,
                    invalid: false,
                    waitList: false,
                  }));
                }}
                color={getTagColor("Invited")}
                active={active.invited}
              />
              <FilterButton
                title={`Confirmed (${stats.confirmed})`}
                onPress={() => {
                  setApplications(
                    allApplications?.filter(
                      (participant) => participant.status === "Confirmed",
                    ) || [],
                  );

                  setActive(() => ({
                    all: false,
                    confirmed: true,
                    rejected: false,
                    underReview: false,
                    invited: false,
                    cancelled: false,
                    invalid: false,
                    waitList: false,
                  }));
                }}
                color={getTagColor("Confirmed")}
                active={active.confirmed}
              />
              <FilterButton
                title={`Cancelled (${stats.cancelled})`}
                onPress={() => {
                  setApplications(
                    allApplications?.filter(
                      (participant) => participant.status === "Cancelled",
                    ) || [],
                  );

                  setActive(() => ({
                    all: false,
                    confirmed: false,
                    rejected: false,
                    underReview: false,
                    invited: false,
                    cancelled: true,
                    invalid: false,
                    waitList: false,
                  }));
                }}
                color={getTagColor("Cancelled")}
                active={active.cancelled}
              />
              <FilterButton
                title={`Rejected (${stats.rejected})`}
                onPress={() => {
                  setApplications(
                    allApplications?.filter(
                      (participant) => participant.status === "Rejected",
                    ) || [],
                  );

                  setActive(() => ({
                    all: false,
                    confirmed: false,
                    rejected: true,
                    underReview: false,
                    invited: false,
                    cancelled: false,
                    invalid: false,
                    waitList: false,
                  }));
                }}
                color={getTagColor("Rejected")}
                active={active.rejected}
              />
              <FilterButton
                title={`Invalid (${stats.rejected})`}
                onPress={() => {
                  setApplications(
                    allApplications?.filter(
                      (participant) => participant.status === "Invalid",
                    ) || [],
                  );

                  setActive(() => ({
                    all: false,
                    confirmed: false,
                    rejected: false,
                    underReview: false,
                    invited: false,
                    cancelled: false,
                    invalid: true,
                    waitList: false,
                  }));
                }}
                color={getTagColor("Invalid")}
                active={active.invalid}
              />
              <FilterButton
                title={`Wait (${stats.waitList})`}
                onPress={() => {
                  setApplications(
                    allApplications?.filter(
                      (participant) => participant.status === "Wait list",
                    ) || [],
                  );

                  setActive(() => ({
                    all: false,
                    confirmed: false,
                    rejected: false,
                    underReview: false,
                    invited: false,
                    cancelled: false,
                    invalid: false,
                    waitList: true,
                  }));
                }}
                color={getTagColor("Wait list")}
                active={active.waitList}
              />
            </ButtonsContainer>
            <ParticipantsNumber>
              Total Participants: {applications?.length}
            </ParticipantsNumber>

            {applications?.length === 0 ? (
              <EmptyPage
                title="No participants"
                subtitle="Anyone have applied to this event... come back soon to have more news"
                image={require("../../../assets/no-participants.webp")}
              />
            ) : (
              <View>
                {applications?.map((application) => (
                  <UserLine key={application.id}>
                    <Username>
                      {application.user.first_name} {application.user.last_name}
                    </Username>
                    <ButtonAndRole>
                      <TagStatus
                        backgroundColor={getTagColor(application.status)}
                      >
                        <Text>{application.status}</Text>
                      </TagStatus>
                      {isAdmin &&
                        (application.status === "Wait list" ||
                          application.status === "Under review") && (
                          <Pressable
                            onPress={() => {
                              setAlertVisible(true);
                              setIdToUpdate(application.id);
                              setUserToUpdate(
                                `${application.user.first_name} ${application.user.last_name}`,
                              );
                            }}
                          >
                            <FontAwesome name="send" size={18} />
                          </Pressable>
                        )}
                    </ButtonAndRole>
                  </UserLine>
                ))}
              </View>
            )}
          </View>
        )}
      </ScrollView>

      <Dialog
        visible={alertVisible}
        title={`What do you want to do with ${userToUpdate} application?`}
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
            title="Invite"
            iconName="send"
            onPress={() => {
              updateStatus("INVITED");
            }}
            color={getTagColor("Invited")}
          />
          <Button
            title="Reject"
            iconName="close"
            onPress={() => {
              updateStatus("REJECTED");
            }}
            color={getTagColor("Rejected")}
          />
          <Button
            title="Wait List"
            iconName="list"
            onPress={() => {
              updateStatus("WAIT_LIST");
            }}
            color={getTagColor("Wait list")}
          />
          <Button
            title="Not valid application"
            iconName="ban"
            onPress={() => {
              updateStatus("INVALID");
            }}
            color={getTagColor("Invalid")}
          />
        </View>
      </Dialog>
      <Toast />
    </Container>
  );
}
