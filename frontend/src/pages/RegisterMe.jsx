import { useState, useEffect } from "react";
import  { useNavigate } from 'react-router';

import { CustomH2MediumTitle } from "../components/Titles";

import { BodyLayout, AccountOption } from "../layouts/Body";
import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { FormLayout } from "../layouts/Form";

import getEnvData from "../config";



function checkDateBirth(dateValue) {

    let error = null;

    if(new Date() - new Date(dateValue) <= 0) {
        error = "Date invalide: date future interdite.";
    }
    else if(new Date() - new Date(dateValue) < 10 * 365 * 24 * 3600 * 1000) {
        error = "Contrainte d'âge: Age minimum requis non respecté.";
    }

    return error;
}



function RegisterMePage() {
    /*

    */

    // ============================== ENVIRONMENT VARIABLES ============================== //
    const settings = getEnvData();
    const BACKEND_API_URL = settings.BACKEND_API_URL
    const LS_USER_INFO_KEY = settings.LS_USER_INFO_KEY;

    // ============================== STATES ============================== //
    const [userInfo, setUserInfo] = useState({ sexe: 'M' });
    const [countries, setCountries] = useState([{}]);
    const [errors, setErrors] = useState({});

    // ==============================  ============================== //
    const navigate = useNavigate();
    const personalFormStructures = [
        {
            format: "input",
            attributes : {
                id: "firstname",
                type: "text",
                title: "Votre nom",
                value: userInfo.firstname || '',
                required: true,
                onChange: (e) => setUserInfo({...userInfo, firstname: e.target.value}),
            },
            text:"Nom"
        },
        {
            format: "input",
            attributes : {
                id: "lastname",
                type: "text",
                title: "Votre prénom",
                value: userInfo.lastname || '',
                required: true,
                onChange: (e) => setUserInfo({...userInfo, lastname: e.target.value}),
            },
            text:"Prénom"
        },
        {
            format: "radio",
            group: {
                name: "sexe",
                items: [
                    {
                        attributes : {
                            id: "Homme",
                            value: "M",
                            checked: userInfo.sexe && userInfo.sexe == 'M',
                            onChange: (e) => setUserInfo({...userInfo, sexe: e.target.value}),
                        },
                        text: "Homme"
                    },
                    {
                        attributes : {
                            id: "Femme",
                            value: "F",
                            checked: userInfo.sexe && userInfo.sexe == 'F',
                            onChange: (e) => setUserInfo({...userInfo, sexe: e.target.value}),
                        },
                        text: "Femme"
                    }
                ],
            },
            text: "Genre"
        },
        {
            format: "input",
            attributes : {
                id: "birth",
                type: "date",
                title: "Votre date de naissance",
                value: userInfo.birth || '',
                required: true,
                errorMessage: errors.dateError || null,
                onChange: (e) => {
                    
                        let userDate = e.target.value;
                        let error = checkDateBirth(userDate);

                        if(error) {
                            setErrors({ ...errors, dateError: error });
                        }
                        else {
                            setErrors({});
                            setUserInfo({ ...userInfo, birth: userDate });
                        }
                    }
            },
            text:"Date de naissance"
        },
        {
            format: "input",
            attributes : {
                id: "email",
                type: "email",
                title: "Votre email actuel",
                value: userInfo.email || '',
                required: true,
                onChange: (e) => setUserInfo({...userInfo, email: e.target.value}),
            },
            text:"Email"
        },
        {
            format: "select",
            attributes : {
                id: "country",
                defaultValue: countries[0].abbr,
                onChange: (e) => setUserInfo({...userInfo, country_id: e.target.value }),
            },
            options: countries,
            text:"Pays d'origine"
        },
        {
            format: "submit",
            attributes: {
                type: "submit",
                title: "Créér mon profil",
            },
            text: "Suivant"
        }
    ];
    

    // ================================ HANDLE API ================================ //
    async function getCountryLists() {
        /*

        */

        const response = await fetch(`${BACKEND_API_URL}/api/v1/utils/countries`);

        if(response.ok) {
            const jsonData = await response.json();
            if(jsonData.success) {
                let allCountries = jsonData.response.map(country => {
                    return {
                        'key': country.abbr,
                        'value': country.id,
                        'text': country.name
                    }
                });
                setCountries(allCountries);
                setUserInfo({ ...userInfo, country_id: allCountries[0].value });
            }
        }
    }


    async function signup(event) {
        /*
        
        */

        event.preventDefault();

        const response = await fetch(
            `${BACKEND_API_URL}/api/v1/register/me`,
            {
                method: 'POST',
                headers: { 'content-type': 'application/json' },
                body: JSON.stringify({ ...userInfo, country_id: parseInt(userInfo.country_id) }),
            }
        );

        if(response.ok) {
            const jsonData = await response.json();
            if(jsonData.success) {
                localStorage.setItem(LS_USER_INFO_KEY, JSON.stringify(jsonData.response));
                navigate('/register/account', { replace: true });
            }
        }
    }

    // ================================ USE EFFECTS ================================ //
    useEffect( () => {
        getCountryLists();
    }, []);

    // ================================ RENDER ================================ //
    return (
        <> 
            <HeaderLayout />
            
            <BodyLayout>
                <CustomH2MediumTitle>
                    Créer un compte sur Task Manager
                </CustomH2MediumTitle>
                <AccountOption linkOption={
                    {
                        "href": '/login',
                        "text": "Se connecter"
                    }
                } >
                    Vous avez déjà un compte ?
                </AccountOption>
                <FormLayout fields={personalFormStructures}
                            onSubmit={signup} />
                <AccountOption linkOption={
                        {
                            "href": '/login',
                            "text": "Se connecter"
                        }
                    } >
                        Vous avez déjà un compte ?
                </AccountOption>
            </BodyLayout>

            <FooterLayout />
        </>
    );
}


export default RegisterMePage;