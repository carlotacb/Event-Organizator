import { ScrollView, View } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import React, { useEffect, useState } from "react";
import Toast from "react-native-toast-message";
import { ConfirmDialog } from "react-native-simple-dialogs";
import {
  cancelApplication,
  getMyApplications,
} from "../utils/api/axiosApplications";
import EmptyPage from "./EmptyPage";
import { getToken } from "../utils/sessionCalls";
import LoadingPage from "./LodingPage";
import CardMyEvents from "./CardMyEvents";
import { ApplicationInformationWithoutUser } from "../utils/interfaces/Applications";

const CardsContainer = styled(View)`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  flex-direction: row;
  margin: 20px 0;
`;

export default function MyEventsPage() {
  const [loading, setLoading] = useState(true);
  const [applications, setApplications] = useState<
    ApplicationInformationWithoutUser[]
  >([]);
  const [trigger, setTrigger] = useState(false);
  const [showCancelAlert, setShowCancelAlert] = useState(false);
  const [idToCancel, setIdToCancel] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const token = await getToken();
      return getMyApplications(token || "");
    };

    fetchData().then((response) => {
      setLoading(false);
      setApplications(response.applications || []);
    });
  }, [trigger]);

  function cancel() {
    const fetchData = async () => {
      const t = await getToken();
      return cancelApplication(t || "", idToCancel);
    };

    fetchData().then((response) => {
      if (response.error) {
        Toast.show({
          type: "error",
          text1: "Error",
          text2: response.error,
          visibilityTime: 8000,
        });
        setShowCancelAlert(false);
      } else {
        setTrigger(!trigger);
        Toast.show({
          type: "success",
          text1: "Success",
          text2: "Your application has been cancelled!",
          visibilityTime: 8000,
        });
        setShowCancelAlert(false);
      }
    });
  }

  return (
    <View>
      {loading ? (
        <LoadingPage />
      ) : (
        <ScrollView>
          {applications.length === 0 ? (
            <EmptyPage
              title="You have no events"
              subtitle="Go back to homepage to see all our available events!"
              image={require("../assets/empty.png")}
            />
          ) : (
            <CardsContainer>
              {applications.map(
                (application: ApplicationInformationWithoutUser) => (
                  <CardMyEvents
                    key={application.id}
                    title={application.event.name}
                    headerImage={application.event.header_image}
                    startDate={application.event.start_date}
                    status={application.status}
                    id={application.id}
                    setIdToCancel={setIdToCancel}
                    setShowCancelAlert={setShowCancelAlert}
                  />
                ),
              )}
            </CardsContainer>
          )}
        </ScrollView>
      )}
      <ConfirmDialog
        title="Are you sure you want to cancel your application?"
        message="Are you sure about that? This only way you can request your participation is by contacting the organizers"
        onTouchOutside={() => setShowCancelAlert(false)}
        visible={showCancelAlert}
        negativeButton={{
          title: "Cancel",
          onPress: () => {
            setShowCancelAlert(false);
          },
          titleStyle: {
            color: "red",
            fontSize: 20,
          },
          style: {
            backgroundColor: "transparent",
            paddingHorizontal: 10,
          },
        }}
        positiveButton={{
          title: "Cancel!",
          onPress: () => {
            cancel();
          },
          titleStyle: {
            color: "blue",
            fontSize: 20,
          },
          style: {
            backgroundColor: "transparent",
            paddingHorizontal: 10,
          },
        }}
        contentInsetAdjustmentBehavior="automatic"
        onRequestClose={() => setShowCancelAlert(false)}
      />
      <Toast />
    </View>
  );
}
