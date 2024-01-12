import React, { useEffect, useState } from "react";
import { Pressable, SafeAreaView, ScrollView, Text, View } from "react-native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
// @ts-ignore
import styled from "styled-components/native";
import Toast from "react-native-toast-message";
import { useLocalSearchParams } from "expo-router";
import LoadingPage from "../../../components/LodingPage";
import { getToken } from "../../../utils/sessionCalls";
import { getParticipants } from "../../../utils/api/axiosApplications";
import { ParticipantsInformation } from "../../../utils/interfaces/Applications";
import EmptyPage from "../../../components/EmptyPage";

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

export default function Id() {
  const { id } = useLocalSearchParams();
  const [loading, setLoading] = useState(true);
  const [applications, setApplications] = useState<
    ParticipantsInformation[] | null
  >(null);

  useEffect(() => {
    const fetchData = async () => {
      const token = await getToken();
      // @ts-ignore
      return getParticipants(token || "", id);
    };

    fetchData().then((response) => {
      console.log(response);
      setLoading(false);
      setApplications(response.participants || []);
    });
  }, []);

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
                      <Pressable onPress={() => {}}>
                        <FontAwesome name="pencil" size={18} />
                      </Pressable>
                    </ButtonAndRole>
                  </UserLine>
                ))}
              </View>
            )}
          </View>
        )}
      </ScrollView>
      <Toast />
    </Container>
  );
}