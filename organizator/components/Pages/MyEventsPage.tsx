import { ScrollView, View } from "react-native";
import React, { useEffect, useState } from "react";
import Toast from "react-native-toast-message";
import { ConfirmDialog } from "react-native-simple-dialogs";
import { useIsFocused } from "@react-navigation/core";
import {
  cancelApplication,
  confirmApplication,
  getMyApplications,
} from "../../utils/api/axiosApplications";
import EmptyPage from "./EmptyPage";
import { getToken } from "../../utils/sessionCalls";
import LoadingPage from "./LodingPage";
import CardMyEvents from "../componentsStyled/Cards/CardMyEvents";
import { ApplicationInformationWithoutUser } from "../../utils/interfaces/Applications";
import { CardsContainer } from "../componentsStyled/Shared/ContainerStyles";

export default function MyEventsPage() {
  const [loading, setLoading] = useState(true);
  const [applications, setApplications] = useState<
    ApplicationInformationWithoutUser[]
  >([]);
  const [trigger, setTrigger] = useState(false);
  const [showCancelAlert, setShowCancelAlert] = useState(false);
  const [idToCancel, setIdToCancel] = useState("");
  const [showConfirmAlert, setShowConfirmAlert] = useState(false);
  const [idToConfirm, setIdToConfirm] = useState("");
  const isFocused = useIsFocused();

  useEffect(() => {
    const fetchData = async () => {
      const token = await getToken();
      return getMyApplications(token || "");
    };

    fetchData().then((response) => {
      setLoading(false);
      setApplications(response.applications || []);
    });
  }, [trigger, isFocused]);

  function cancelParticipation() {
    const fetchData = async () => {
      const tkn = await getToken();
      return cancelApplication(tkn || "", idToCancel);
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

  function confirmParticipation() {
    const fetchData = async () => {
      const tkn = await getToken();
      return confirmApplication(tkn || "", idToConfirm);
    };

    fetchData().then((response) => {
      if (response.error) {
        Toast.show({
          type: "error",
          text1: "Error",
          text2: response.error,
          visibilityTime: 8000,
        });
        setShowConfirmAlert(false);
      } else {
        setTrigger(!trigger);
        Toast.show({
          type: "success",
          text1: "Success",
          text2: "Your spot in the event is now confirmed!",
          visibilityTime: 8000,
        });
        setShowConfirmAlert(false);
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
              image={require("../../assets/empty.png")}
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
                    setIdToConfirm={setIdToConfirm}
                    setShowConfirmAlert={setShowConfirmAlert}
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
            setIdToCancel("");
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
            cancelParticipation();
            setShowCancelAlert(false);
            setIdToCancel("");
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
        onRequestClose={() => {
          setShowCancelAlert(false);
          setIdToCancel("");
        }}
      />

      <ConfirmDialog
        title="Yeyy!! We are happy you can come"
        message="You can cancel your participation at any time. We hope to see you at the event."
        onTouchOutside={() => {
          setShowConfirmAlert(false);
          setIdToConfirm("");
        }}
        visible={showConfirmAlert}
        positiveButton={{
          title: "Confirm!",
          onPress: () => {
            confirmParticipation();
            setShowConfirmAlert(false);
            setIdToConfirm("");
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
        onRequestClose={() => {
          setShowConfirmAlert(false);
          setIdToConfirm("");
        }}
      />
      <Toast />
    </View>
  );
}
