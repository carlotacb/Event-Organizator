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
} from "../../../utils/api/axiosUsers";
import { getToken, removeToken } from "../../../utils/sessionCalls";
import { UserInformation, UserRoles } from "../../../utils/interfaces/Users";
import Input from "../../../components/componentsStyled/Forms/Input";
import LoadingPage from "../../../components/Pages/LodingPage";
import InputLabel from "../../../components/componentsStyled/Forms/InputLabel";
import FilterButton from "../../../components/componentsStyled/Buttons/FilterButtons";
import {
  checkDateBirth,
  checkDateGraduation,
} from "../../../utils/util-functions";

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

const Tag = styled(View)<{ backgroundColor: string }>`
  background-color: ${(props: { backgroundColor: string }) =>
    props.backgroundColor};
  border: 2px solid #233277;
  border-radius: 100px;
  padding: 5px 15px;
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 5px;
`;

const CreateButtonContainer = styled(View)`
  padding-top: 20px;
  padding-bottom: 20px;
  align-items: center;
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
`;

const CreateButton = styled(Pressable)`
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 10px 30px;
  border-radius: 20px;
  gap: 10px;
  background-color: #233277;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
`;

const UpgradeButton = styled(Pressable)`
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 10px 30px;
  border-radius: 20px;
  gap: 10px;
  background-color: #58a659;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
`;

const CreateButtonText = styled.Text`
  font-size: 18px;
  color: white;
  font-weight: bold;
`;

const ButtonsWSContainer = styled(View)<{ withoutMargin: boolean }>`
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: flex-start;
  margin-bottom: ${(props: { withoutMargin: boolean }) =>
    props.withoutMargin ? "0px" : "20px"};
`;

export default function Index() {
  const [loading, setLoading] = React.useState(true);
  const [token, setToken] = React.useState<string | null>(null);
  const [userInformation, setUserInformation] =
    React.useState<UserInformation | null>(null);
  const [inputs, setInputs] = useState({
    firstName: "",
    lastName: "",
    bio: "",
    tShirtSize: "",
    alimentaryRestrictions: "",
    dateOfBirth: "",
    gender: "",
    github: "",
    linkedin: "",
    devpost: "",
    webpage: "",
    university: "",
    degree: "",
    expectedGraduation: "",
    currentJobRole: "",
  });
  const [errors, setErrors] = useState({
    firstName: undefined,
    lastName: undefined,
    bio: undefined,
    tShirtSize: undefined,
    alimentaryRestrictions: undefined,
    dateOfBirth: undefined,
    gender: undefined,
    github: undefined,
    linkedin: undefined,
    devpost: undefined,
    webpage: undefined,
    university: undefined,
    degree: undefined,
    expectedGraduation: undefined,
    currentJobRole: undefined,
  });
  const [activeTShirtSize, setActiveTShirtSize] = useState({
    XS: false,
    S: false,
    M: false,
    L: false,
    XL: false,
    XXL: false,
  });
  const [activeGender, setActiveGender] = useState({
    FEMALE: false,
    MALE: false,
    NO_BINARY: false,
    PREFER_NOT_TO_SAY: false,
  });
  const [activeDiet, setActiveDiet] = useState({
    VEGAN: false,
    VEGETARIAN: false,
    GLUTEN_FREE: false,
    OTHER: false,
    NOTHING: false,
  });
  const [isWorking, setIsWorking] = React.useState(false);
  const [isStudying, setIsStudying] = React.useState(true);
  const [activeStatus, setActiveStatus] = React.useState({
    study: true,
    work: false,
    nothing: false,
  });

  useEffect(() => {
    const fetchData = async () => {
      const tkn = await getToken();
      if (tkn !== null) {
        setToken(tkn);
      }

      return getMyInformation(tkn);
    };

    fetchData().then((response) => {
      setLoading(false);

      if (response.error) {
        removeToken();
        router.replace("/login");
      } else {
        setUserInformation(response.userInformation);
        setActiveTShirtSize({
          XS: response.userInformation?.tShirtSize === "XS",
          S: response.userInformation?.tShirtSize === "S",
          M: response.userInformation?.tShirtSize === "M",
          L: response.userInformation?.tShirtSize === "L",
          XL: response.userInformation?.tShirtSize === "XL",
          XXL: response.userInformation?.tShirtSize === "XXL",
        });
        setActiveGender({
          FEMALE: response.userInformation?.gender === "Female",
          MALE: response.userInformation?.gender === "Male",
          NO_BINARY: response.userInformation?.gender === "No-binary",
          PREFER_NOT_TO_SAY:
            response.userInformation?.gender === "Prefer not to say",
        });
        setActiveDiet({
          VEGAN: response.userInformation?.alimentaryRestrictions === "Vegan",
          VEGETARIAN:
            response.userInformation?.alimentaryRestrictions === "Vegetarian",
          GLUTEN_FREE:
            response.userInformation?.alimentaryRestrictions === "Gluten free",
          OTHER:
            response.userInformation?.alimentaryRestrictions !== "Vegan" &&
            response.userInformation?.alimentaryRestrictions !== "Vegetarian" &&
            response.userInformation?.alimentaryRestrictions !==
              "Gluten free" &&
            response.userInformation?.alimentaryRestrictions !==
              "No restrictions" &&
            response.userInformation?.alimentaryRestrictions !== null,
          NOTHING:
            response.userInformation?.alimentaryRestrictions ===
            "No restrictions",
        });
        setInputs({
          firstName: response.userInformation?.firstName || "",
          lastName: response.userInformation?.lastName || "",
          bio: response.userInformation?.bio || "",
          tShirtSize: response.userInformation?.tShirtSize || "",
          alimentaryRestrictions:
            response.userInformation?.alimentaryRestrictions || "",
          dateOfBirth: response.userInformation?.dateOfBirth || "",
          gender: response.userInformation?.gender || "",
          github: response.userInformation?.github || "",
          linkedin: response.userInformation?.linkedin || "",
          devpost: response.userInformation?.devpost || "",
          webpage: response.userInformation?.webpage || "",
          university: response.userInformation?.university || "",
          degree: response.userInformation?.degree || "",
          expectedGraduation:
            response.userInformation?.expectedGraduation || "",
          currentJobRole: response.userInformation?.currentJobRole || "",
        });
      }
    });
  }, []);

  const validate = () => {
    let isValid = true;

    if (inputs.firstName === "") {
      handleError("First name is required", "firstName");
      isValid = false;
    } else {
      handleError(undefined, "firstName");
    }

    if (inputs.lastName === "") {
      handleError("Last name is required", "lastName");
      isValid = false;
    } else {
      handleError(undefined, "lastName");
    }

    if (inputs.bio === "") {
      handleError("Biography is required", "bio");
      isValid = false;
    } else {
      handleError(undefined, "bio");
    }

    if (!inputs.dateOfBirth) {
      handleError("Please enter your date birth", "dateOfBirth");
      isValid = false;
    } else {
      const dateChecker = checkDateBirth(inputs.dateOfBirth);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "dateOfBirth");
        isValid = false;
      } else {
        handleError(undefined, "dateOfBirth");
      }
    }

    if (!inputs.alimentaryRestrictions) {
      handleError(
        "Please enter your alimentary restrictions",
        "alimentaryRestrictions",
      );
      isValid = false;
    } else {
      handleError(undefined, "alimentaryRestrictions");
    }

    if (!inputs.expectedGraduation && isStudying) {
      handleError("Please enter your graduation year", "expectedGraduation");
      isValid = false;
    } else {
      const dateChecker = checkDateGraduation(inputs.expectedGraduation);
      if (!dateChecker.valid && isStudying) {
        handleError(dateChecker.error, "expectedGraduation");
        isValid = false;
      } else {
        handleError(undefined, "expectedGraduations");
      }
    }

    if (!inputs.currentJobRole && isWorking) {
      handleError("Please enter your current job role", "currentJobRole");
      isValid = false;
    } else {
      handleError(undefined, "currentJobRole");
    }

    if (!inputs.university && isStudying) {
      handleError("Please enter your university", "university");
      isValid = false;
    } else {
      handleError(undefined, "university");
    }

    if (!inputs.degree && isStudying) {
      handleError("Please enter your degree", "degree");
      isValid = false;
    } else {
      handleError(undefined, "degree");
    }

    if (isValid) editProfile();
  };

  const editProfile = () => {
    setLoading(true);

    updateMyInformation(inputs, token || "", isStudying, isWorking).then(
      (response) => {
        if (response.error) {
          if (
            response.error === "Invalid token" ||
            response.error === "Unauthorized" ||
            response.error === "User does not exist"
          ) {
            removeToken();
            router.replace("/login");
          }
          setLoading(false);
          Toast.show({
            type: "error",
            text1: "Error",
            text2: response.error,
            visibilityTime: 8000,
          });
        } else {
          setLoading(false);
          Toast.show({
            type: "success",
            text1: "Success",
            text2: "Your profile has been updated correctly",
            visibilityTime: 8000,
          });
        }
      },
    );
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
                label="Date of birth"
                iconName="calendar"
                required
                value={inputs.dateOfBirth}
                onChangeText={(text) => handleOnChange(text, "dateOfBirth")}
                placeholder="DD/MM/YYYY"
                placeholderTextColor="#969696"
                error={errors.dateOfBirth}
              />
              <Input
                label="Biography"
                iconName="pencil"
                multiline
                numberOfLines={4}
                required
                value={inputs.bio}
                onChangeText={(text) => handleOnChange(text, "bio")}
                error={errors.bio}
              />
              <InputLabel label="Currently I'm..." />
              <ButtonsWSContainer>
                <FilterButton
                  title="Study"
                  onPress={() => {
                    setActiveStatus({
                      study: true,
                      work: false,
                      nothing: false,
                    });
                    setIsStudying(true);
                    setIsWorking(false);
                  }}
                  color="dimgray"
                  active={activeStatus.study}
                />
                <FilterButton
                  title="Work"
                  onPress={() => {
                    setActiveStatus({
                      study: false,
                      work: true,
                      nothing: false,
                    });
                    setIsStudying(false);
                    setIsWorking(true);
                  }}
                  color="dimgray"
                  active={activeStatus.work}
                />
                <FilterButton
                  title="Nothing"
                  onPress={() => {
                    setActiveStatus({
                      study: false,
                      work: false,
                      nothing: true,
                    });
                    setIsStudying(false);
                    setIsWorking(false);
                  }}
                  color="dimgray"
                  active={activeStatus.nothing}
                />
              </ButtonsWSContainer>

              {isWorking && (
                <Input
                  label="Current Job Role"
                  iconName="briefcase"
                  required
                  value={inputs.currentJobRole}
                  onChangeText={(text) =>
                    handleOnChange(text, "currentJobRole")
                  }
                  error={errors.currentJobRole}
                />
              )}

              {isStudying && (
                <>
                  <Input
                    label="University"
                    iconName="university"
                    required
                    value={inputs.university}
                    onChangeText={(text) => handleOnChange(text, "university")}
                    error={errors.university}
                  />
                  <Input
                    label="Degree"
                    iconName="book"
                    required
                    value={inputs.degree}
                    onChangeText={(text) => handleOnChange(text, "degree")}
                    error={errors.degree}
                  />
                  <Input
                    label="Graduation year"
                    iconName="graduation-cap"
                    required
                    value={inputs.expectedGraduation}
                    onChangeText={(text) =>
                      handleOnChange(text, "expectedGraduation")
                    }
                    placeholder="DD/MM/YYYY"
                    placeholderTextColor="#969696"
                    error={errors.expectedGraduation}
                  />
                </>
              )}

              <InputLabel label="T-shirt size" />
              <ButtonsWSContainer>
                <FilterButton
                  title="XS"
                  onPress={() => {
                    setActiveTShirtSize({
                      XS: true,
                      S: false,
                      M: false,
                      L: false,
                      XL: false,
                      XXL: false,
                    });
                    handleOnChange("XS", "tShirtSize");
                  }}
                  color="dimgray"
                  active={activeTShirtSize.XS}
                />
                <FilterButton
                  title="S"
                  onPress={() => {
                    setActiveTShirtSize({
                      XS: false,
                      S: true,
                      M: false,
                      L: false,
                      XL: false,
                      XXL: false,
                    });
                    handleOnChange("S", "tShirtSize");
                  }}
                  color="dimgray"
                  active={activeTShirtSize.S}
                />
                <FilterButton
                  title="M"
                  onPress={() => {
                    setActiveTShirtSize({
                      XS: false,
                      S: false,
                      M: true,
                      L: false,
                      XL: false,
                      XXL: false,
                    });
                    handleOnChange("M", "tShirtSize");
                  }}
                  color="dimgray"
                  active={activeTShirtSize.M}
                />
                <FilterButton
                  title="L"
                  onPress={() => {
                    setActiveTShirtSize({
                      XS: false,
                      S: false,
                      M: false,
                      L: true,
                      XL: false,
                      XXL: false,
                    });
                    handleOnChange("L", "tShirtSize");
                  }}
                  color="dimgray"
                  active={activeTShirtSize.L}
                />
                <FilterButton
                  title="XL"
                  onPress={() => {
                    setActiveTShirtSize({
                      XS: false,
                      S: false,
                      M: false,
                      L: false,
                      XL: true,
                      XXL: false,
                    });
                    handleOnChange("XL", "tShirtSize");
                  }}
                  color="dimgray"
                  active={activeTShirtSize.XL}
                />
                <FilterButton
                  title="XXL"
                  onPress={() => {
                    setActiveTShirtSize({
                      XS: false,
                      S: false,
                      M: false,
                      L: false,
                      XL: false,
                      XXL: true,
                    });
                    handleOnChange("XXL", "tShirtSize");
                  }}
                  color="dimgray"
                  active={activeTShirtSize.XXL}
                />
              </ButtonsWSContainer>
              <InputLabel label="Gender" />
              <ButtonsWSContainer>
                <FilterButton
                  title="Female"
                  onPress={() => {
                    setActiveGender({
                      FEMALE: true,
                      MALE: false,
                      NO_BINARY: false,
                      PREFER_NOT_TO_SAY: false,
                    });
                    handleOnChange("FEMALE", "gender");
                  }}
                  color="dimgray"
                  active={activeGender.FEMALE}
                />
                <FilterButton
                  title="Male"
                  onPress={() => {
                    setActiveGender({
                      FEMALE: false,
                      MALE: true,
                      NO_BINARY: false,
                      PREFER_NOT_TO_SAY: false,
                    });
                    handleOnChange("MALE", "gender");
                  }}
                  color="dimgray"
                  active={activeGender.MALE}
                />
                <FilterButton
                  title="Non-binary"
                  onPress={() => {
                    setActiveGender({
                      FEMALE: false,
                      MALE: false,
                      NO_BINARY: true,
                      PREFER_NOT_TO_SAY: false,
                    });
                    handleOnChange("NO_BINARY", "gender");
                  }}
                  color="dimgray"
                  active={activeGender.NO_BINARY}
                />
                <FilterButton
                  title="Won't say"
                  onPress={() => {
                    setActiveGender({
                      FEMALE: false,
                      MALE: false,
                      NO_BINARY: false,
                      PREFER_NOT_TO_SAY: true,
                    });
                    handleOnChange("PREFER_NOT_TO_SAY", "gender");
                  }}
                  color="dimgray"
                  active={activeGender.PREFER_NOT_TO_SAY}
                />
              </ButtonsWSContainer>
              <InputLabel label="Alimentary restriction" required />
              <ButtonsWSContainer withoutMargin={activeDiet.OTHER}>
                <FilterButton
                  title="Vegan"
                  onPress={() => {
                    setActiveDiet({
                      VEGAN: true,
                      VEGETARIAN: false,
                      GLUTEN_FREE: false,
                      OTHER: false,
                      NOTHING: false,
                    });
                    handleOnChange("Vegan", "alimentaryRestrictions");
                  }}
                  color="dimgray"
                  active={activeDiet.VEGAN}
                />
                <FilterButton
                  title="Vegetarian"
                  onPress={() => {
                    setActiveDiet({
                      VEGAN: false,
                      VEGETARIAN: true,
                      GLUTEN_FREE: false,
                      OTHER: false,
                      NOTHING: false,
                    });
                    handleOnChange("Vegeterian", "alimentaryRestrictions");
                  }}
                  color="dimgray"
                  active={activeDiet.VEGETARIAN}
                />
                <FilterButton
                  title="Gluten free"
                  onPress={() => {
                    setActiveDiet({
                      VEGAN: false,
                      VEGETARIAN: false,
                      GLUTEN_FREE: true,
                      OTHER: false,
                      NOTHING: false,
                    });
                    handleOnChange("Gluten free", "alimentaryRestrictions");
                  }}
                  color="dimgray"
                  active={activeDiet.GLUTEN_FREE}
                />
                <FilterButton
                  title="Nothing"
                  onPress={() => {
                    setActiveDiet({
                      VEGAN: false,
                      VEGETARIAN: false,
                      GLUTEN_FREE: false,
                      NOTHING: true,
                      OTHER: false,
                    });
                    handleOnChange("No restrictions", "alimentaryRestrictions");
                  }}
                  color="dimgray"
                  active={activeDiet.NOTHING}
                />
                <FilterButton
                  title="Other"
                  onPress={() => {
                    setActiveDiet({
                      VEGAN: false,
                      VEGETARIAN: false,
                      GLUTEN_FREE: false,
                      NOTHING: false,
                      OTHER: true,
                    });
                    handleOnChange("", "alimentaryRestrictions");
                  }}
                  color="dimgray"
                  active={activeDiet.OTHER}
                />
              </ButtonsWSContainer>
              {activeDiet.OTHER ? (
                <Input
                  iconName="cutlery"
                  value={inputs.alimentaryRestrictions}
                  onChangeText={(text) =>
                    handleOnChange(text, "alimentaryRestrictions")
                  }
                  error={errors.alimentaryRestrictions}
                />
              ) : null}

              <Input
                label="GitHub"
                iconName="github-square"
                value={inputs.github}
                onChangeText={(text) => handleOnChange(text, "github")}
                error={errors.github}
              />
              <Input
                label="LinkedIn"
                iconName="linkedin-square"
                value={inputs.linkedin}
                onChangeText={(text) => handleOnChange(text, "linkedin")}
                error={errors.linkedin}
              />
              <Input
                label="Devpost"
                iconName="code"
                value={inputs.devpost}
                onChangeText={(text) => handleOnChange(text, "devpost")}
                error={errors.devpost}
              />
              <Input
                label="Webpage"
                iconName="link"
                value={inputs.webpage}
                onChangeText={(text) => handleOnChange(text, "webpage")}
                error={errors.webpage}
              />
            </InputsContainer>
          </>
        )}
        <Toast />
      </ScrollView>

      <CreateButtonContainer>
        <UpgradeButton onPress={validate}>
          <FontAwesome name="save" size={20} color="white" />
          <CreateButtonText>Update</CreateButtonText>
        </UpgradeButton>
        {userInformation?.role === UserRoles.ORGANIZER_ADMIN && (
          <CreateButton onPress={() => router.push("/profile/users")}>
            <FontAwesome name="user" size={20} color="white" />
            <CreateButtonText>All users</CreateButtonText>
          </CreateButton>
        )}
      </CreateButtonContainer>
    </Container>
  );
}
