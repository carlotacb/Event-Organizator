import React, { useEffect, useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
  View,
} from "react-native";
import { router } from "expo-router";
// @ts-ignore
import styled from "styled-components/native";
import Toast from "react-native-toast-message";
import { useIsFocused } from "@react-navigation/core";
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
  getBackGroundColorForRole,
  parseDegreeStatus,
  parseDiet,
  parseGender,
  parseRole,
} from "../../../utils/util-functions";
import { Title } from "../../../components/componentsStyled/Shared/TextStyles";
import InformativeChip from "../../../components/componentsStyled/Chips/InformativeChip";
import {
  ButtonsRowContainer,
  RadioButtonContainer,
} from "../../../components/componentsStyled/Shared/ContainerStyles";
import Button from "../../../components/componentsStyled/Buttons/ButtonWithIcon";
import { systemColors } from "../../../components/componentsStyled/tokens";
import {
  handleError,
  handleOnChange,
} from "../../../components/componentsStyled/Forms/utilFunctions";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

const ContainerTags = styled.View`
  display: flex;
  flex-direction: row;
  align-items: center;
  align-content: center;
  justify-content: flex-end;
  gap: 30px;
  margin-bottom: 30px;
`;

const TextRowLine = styled.View`
  display: flex;
  flex-direction: row;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  gap: 20px;
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

  const [activeStatus, setActiveStatus] = React.useState({
    study: true,
    work: false,
    nothing: false,
  });
  const careerStatus = ["study", "work", "nothing"];
  const [isWorking, setIsWorking] = React.useState(false);
  const [isStudying, setIsStudying] = React.useState(true);

  const [activeTShirtSize, setActiveTShirtSize] = useState({
    XS: false,
    S: false,
    M: false,
    L: false,
    XL: false,
    XXL: false,
  });
  const sizeButtons = ["XS", "S", "M", "L", "XL", "XXL"];

  const [activeGender, setActiveGender] = useState({
    FEMALE: false,
    MALE: false,
    NO_BINARY: false,
    PREFER_NOT_TO_SAY: false,
  });
  const genderButtons = ["FEMALE", "MALE", "NO_BINARY", "PREFER_NOT_TO_SAY"];

  const [activeDiet, setActiveDiet] = useState({
    VEGAN: false,
    VEGETARIAN: false,
    GLUTEN_FREE: false,
    OTHER: false,
    NOTHING: false,
  });
  const dietButtons = [
    "VEGAN",
    "VEGETARIAN",
    "GLUTEN_FREE",
    "NOTHING",
    "OTHER",
  ];

  const isFocused = useIsFocused();

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
  }, [isFocused]);

  const validate = () => {
    let isValid = true;

    if (inputs.firstName === "") {
      handleError("First name is required", "firstName", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "firstName", setErrors);
    }

    if (inputs.lastName === "") {
      handleError("Last name is required", "lastName", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "lastName", setErrors);
    }

    if (inputs.bio === "") {
      handleError("Biography is required", "bio", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "bio", setErrors);
    }

    if (!inputs.dateOfBirth) {
      handleError("Please enter your date birth", "dateOfBirth", setErrors);
      isValid = false;
    } else {
      const dateChecker = checkDateBirth(inputs.dateOfBirth);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "dateOfBirth", setErrors);
        isValid = false;
      } else {
        handleError(undefined, "dateOfBirth", setErrors);
      }
    }

    if (!inputs.alimentaryRestrictions) {
      handleError(
        "Please enter your alimentary restrictions",
        "alimentaryRestrictions",
        setErrors,
      );
      isValid = false;
    } else {
      handleError(undefined, "alimentaryRestrictions", setErrors);
    }

    if (!inputs.expectedGraduation && isStudying) {
      handleError(
        "Please enter your graduation year",
        "expectedGraduation",
        setErrors,
      );
      isValid = false;
    } else {
      const dateChecker = checkDateGraduation(inputs.expectedGraduation);
      if (!dateChecker.valid && isStudying) {
        handleError(dateChecker.error, "expectedGraduation", setErrors);
        isValid = false;
      } else {
        handleError(undefined, "expectedGraduations", setErrors);
      }
    }

    if (!inputs.currentJobRole && isWorking) {
      handleError(
        "Please enter your current job role",
        "currentJobRole",
        setErrors,
      );
      isValid = false;
    } else {
      handleError(undefined, "currentJobRole", setErrors);
    }

    if (!inputs.university && isStudying) {
      handleError("Please enter your university", "university", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "university", setErrors);
    }

    if (!inputs.degree && isStudying) {
      handleError("Please enter your degree", "degree", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "degree", setErrors);
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

  return (
    <Container>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
      >
        <ScrollView contentContainerStyle={{ padding: 20 }}>
          {loading ? (
            <LoadingPage />
          ) : (
            <>
              <ContainerTags>
                {userInformation?.role === UserRoles.ORGANIZER_ADMIN && (
                  <Button
                    title="See all users"
                    iconName="users"
                    onPress={() => router.push("/profile/users")}
                    color={systemColors.action}
                  />
                )}

                <Button
                  title="Logout"
                  onPress={loggingOut}
                  color={systemColors.destroy}
                  iconName="sign-out"
                />
              </ContainerTags>

              <TextRowLine>
                <Title>Hello, {userInformation?.username}</Title>
                <InformativeChip
                  fontSize="15px"
                  name={parseRole(userInformation?.role || "")}
                  backgroundColor={getBackGroundColorForRole(
                    userInformation?.role || "",
                  )}
                />
              </TextRowLine>
              <View
                style={{
                  marginTop: 10,
                  alignItems: "baseline",
                  marginBottom: 30,
                }}
              >
                <InformativeChip
                  name={userInformation?.email || ""}
                  backgroundColor={systemColors.backgroundGrey}
                  fontSize="15px"
                />
              </View>

              <Input
                label="First Name"
                iconName="id-badge"
                required
                value={inputs.firstName}
                onChangeText={(text) =>
                  handleOnChange(text, "firstName", setInputs)
                }
                error={errors.firstName}
              />
              <Input
                label="Last Name"
                iconName="id-badge"
                required
                value={inputs.lastName}
                onChangeText={(text) =>
                  handleOnChange(text, "lastName", setInputs)
                }
                error={errors.lastName}
              />
              <Input
                label="Date of birth"
                iconName="calendar"
                required
                value={inputs.dateOfBirth}
                onChangeText={(text) =>
                  handleOnChange(text, "dateOfBirth", setInputs)
                }
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
                onChangeText={(text) => handleOnChange(text, "bio", setInputs)}
                error={errors.bio}
              />
              <InputLabel label="Currently I'm... (select one of the options)" />
              <RadioButtonContainer>
                {careerStatus.map((status) => (
                  <FilterButton
                    key={parseDegreeStatus(status)}
                    title={status}
                    onPress={() => {
                      setActiveStatus({
                        study: status === "study",
                        work: status === "work",
                        nothing: status === "nothing",
                      });
                      setIsStudying(status === "study");
                      setIsWorking(status === "work");
                    }}
                    color="dimgray"
                    // @ts-ignore
                    active={activeStatus[status]}
                  />
                ))}
              </RadioButtonContainer>

              {isWorking && (
                <Input
                  label="Current Job Role"
                  iconName="briefcase"
                  required
                  value={inputs.currentJobRole}
                  onChangeText={(text) =>
                    handleOnChange(text, "currentJobRole", setInputs)
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
                    onChangeText={(text) =>
                      handleOnChange(text, "university", setInputs)
                    }
                    error={errors.university}
                  />
                  <Input
                    label="Degree"
                    iconName="book"
                    required
                    value={inputs.degree}
                    onChangeText={(text) =>
                      handleOnChange(text, "degree", setInputs)
                    }
                    error={errors.degree}
                  />
                  <Input
                    label="Graduation year"
                    iconName="graduation-cap"
                    required
                    value={inputs.expectedGraduation}
                    onChangeText={(text) =>
                      handleOnChange(text, "expectedGraduation", setInputs)
                    }
                    placeholder="DD/MM/YYYY"
                    placeholderTextColor="#969696"
                    error={errors.expectedGraduation}
                  />
                </>
              )}

              <InputLabel label="T-shirt size" />
              <RadioButtonContainer>
                {sizeButtons.map((size) => (
                  <FilterButton
                    key={size}
                    title={size}
                    onPress={() => {
                      setActiveTShirtSize({
                        XS: size === "XS",
                        S: size === "S",
                        M: size === "M",
                        L: size === "L",
                        XL: size === "XL",
                        XXL: size === "XXL",
                      });
                      handleOnChange(size, "tShirtSize", setInputs);
                    }}
                    color="dimgray"
                    // @ts-ignore
                    active={activeTShirtSize[size]}
                  />
                ))}
              </RadioButtonContainer>
              <InputLabel label="Gender" />
              <RadioButtonContainer>
                {genderButtons.map((gender) => (
                  <FilterButton
                    key={gender}
                    title={parseGender(gender)}
                    onPress={() => {
                      setActiveGender({
                        FEMALE: gender === "FEMALE",
                        MALE: gender === "MALE",
                        NO_BINARY: gender === "NO_BINARY",
                        PREFER_NOT_TO_SAY: gender === "PREFER_NOT_TO_SAY",
                      });
                      handleOnChange(gender, "gender", setInputs);
                    }}
                    color="dimgray"
                    // @ts-ignore
                    active={activeGender[gender]}
                  />
                ))}
              </RadioButtonContainer>
              <InputLabel label="Alimentary restriction" required />

              <RadioButtonContainer withoutMargin={activeDiet.OTHER}>
                {dietButtons.map((diet) => (
                  <FilterButton
                    key={diet}
                    title={parseDiet(diet)}
                    onPress={() => {
                      setActiveDiet({
                        VEGAN: diet === "VEGAN",
                        VEGETARIAN: diet === "VEGETARIAN",
                        GLUTEN_FREE: diet === "GLUTEN_FREE",
                        NOTHING: diet === "NOTHING",
                        OTHER: diet === "OTHER",
                      });
                      handleOnChange(
                        parseDiet(diet) === "Other" ? "" : parseDiet(diet),
                        "alimentaryRestrictions",
                        setInputs,
                      );
                    }}
                    color="dimgray"
                    // @ts-ignore
                    active={activeDiet[diet]}
                  />
                ))}
              </RadioButtonContainer>
              {activeDiet.OTHER ? (
                <Input
                  iconName="cutlery"
                  value={inputs.alimentaryRestrictions}
                  onChangeText={(text) =>
                    handleOnChange(text, "alimentaryRestrictions", setInputs)
                  }
                  error={errors.alimentaryRestrictions}
                />
              ) : null}

              <Input
                label="GitHub"
                iconName="github-square"
                value={inputs.github}
                onChangeText={(text) =>
                  handleOnChange(text, "github", setInputs)
                }
                error={errors.github}
              />
              <Input
                label="LinkedIn"
                iconName="linkedin-square"
                value={inputs.linkedin}
                onChangeText={(text) =>
                  handleOnChange(text, "linkedin", setInputs)
                }
                error={errors.linkedin}
              />
              <Input
                label="Devpost"
                iconName="code"
                value={inputs.devpost}
                onChangeText={(text) =>
                  handleOnChange(text, "devpost", setInputs)
                }
                error={errors.devpost}
              />
              <Input
                label="Webpage"
                iconName="link"
                value={inputs.webpage}
                onChangeText={(text) =>
                  handleOnChange(text, "webpage", setInputs)
                }
                error={errors.webpage}
              />
              <ButtonsRowContainer>
                <Button
                  title="Update profile"
                  onPress={validate}
                  color={systemColors.accept}
                  iconName="save"
                />
              </ButtonsRowContainer>
            </>
          )}
        </ScrollView>
      </KeyboardAvoidingView>
      <Toast />
    </Container>
  );
}
