import { useState, useEffect } from "react";

import { CustomH2MediumTitle } from "../components/Titles";

import { BodyLayout, AccountOption } from "../layouts/Body";
import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { FormLayout } from "../layouts/Form";



function RegisterMePage() {
    /*

    */

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_MAIN_URL;

    const [userInfo, setUserInfo] = useState({
        firstname: "",
        lastname: "",
        sexe: "M",
        birth: "",
        email: "",
        country_id: 0,
    })

    const [countries, setCountries] = useState([{
        key: '',
        value: '',
        name: '',
        text: ''
    }]);

    const personalFormStructures = [
        {
            format: "input",
            attributes : {
                id: "firstname",
                type: "text",
                title: "Votre nom",
                value: userInfo.firstname,
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
                value: userInfo.lastname,
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
                            checked: userInfo.sexe === "M",
                            onChange: (e) => setUserInfo({...userInfo, sexe: e.target.value}),
                        },
                        text: "Homme"
                    },
                    {
                        attributes : {
                            id: "Femme",
                            value: "F",
                            checked: userInfo.sexe === "F",
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
                value: userInfo.birth,
                required: true,
                onChange: (e) => setUserInfo({...userInfo, birth: e.target.value}),
            },
            text:"Date de naissance"
        },
        {
            format: "input",
            attributes : {
                id: "email",
                type: "email",
                title: "Votre email actuel",
                value: userInfo.email,
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
    

    // ================================ HANDLE SUBMIT ================================ //
    async function getCoutryLists() {
        const response = await fetch(`${BACKEND_API_URL}/api/v1/utils/countries`);

        if(response.ok) {
            const jsonData = await response.json();
            if(jsonData.success) {
                let allCountries = jsonData.response.map(country => {
                    return {
                        'key': country.id,
                        'value': country.id,
                        'name': country.abbr,
                        'text': country.name
                    }
                });
                setCountries(allCountries)
                setUserInfo({ ...userInfo, country_id: allCountries[0].value })
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
                localStorage.setItem('registerMe', JSON.stringify(jsonData.response));
            }
        }
    }

    useEffect( () => {
        getCoutryLists();
    }, []);
    

    return (
        <> 
            <HeaderLayout />
            
            <BodyLayout>
                <CustomH2MediumTitle>
                    Créer un compte Task Manager
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