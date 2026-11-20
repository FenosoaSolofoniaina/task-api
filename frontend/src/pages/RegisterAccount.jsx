import { useState } from "react";
import  { useNavigate, Navigate } from 'react-router';

import { CustomH2MediumTitle } from "../components/Titles";

import { BodyLayout } from "../layouts/Body";
import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { FormLayout } from "../layouts/Form";

import getEnvData from "../config";



function validatePassword(password) {
    let errors = [];

    if (password.length < 8) {
        errors.push("Le mot de passe doit contenir au moins 8 caractères.");
    }
    if (/[À-ÖØ-öø-ÿ]/.test(password)) {
        errors.push("Les lettres accentuées ne sont pas autorisées.");
    }

    return errors;
}


function checkPassword(password, copyPassword) {
    let error = null;

    if (copyPassword.trim() && password != copyPassword) {
        error = "Les deux mots de passes doivent être identiques.";
    }

    return error;
}


function RegisterAccountPAge() {
    /*

    */


    // ============================== ENVIRONMENT VARIABLES ============================== //
    const settings = getEnvData();
    const BACKEND_API_URL = settings.BACKEND_API_URL;
    const LS_USER_INFO_KEY = settings.LS_USER_INFO_KEY;
    
    // ============================== STATES ============================== //
    const [userAccount, setUserAccount] = useState({});
    const [showPassword, setShowPassword] = useState(false);
    const [errors,  setErrors] = useState({});
    
    // ==============================  ============================== //
    let isUserInfoExist = localStorage.getItem(LS_USER_INFO_KEY);
    const navigate = useNavigate();
    const accountFormStructures = [
        {
            format: "input",
            attributes : {
                id: "identity",
                type: "text",
                title: "Identité",
                value: userAccount.identity || '',
                required: true,
                onChange: (e) => setUserAccount({ ...userAccount, identity: e.target.value }),
            },
            text:"Identité"
        },
        {
            format: "input",
            attributes : {
                id: "password",
                type: showPassword ? "text" : "password",
                title: "Mot de passe",
                required: true,
                errorMessage: errors.passwordError,
                onChange: (e) => {
                    let userPassword = e.target.value;
                    let passwordErrors = validatePassword(userPassword);
                    if(passwordErrors.length) {
                        setErrors({ ...errors, passwordError: passwordErrors.join(' ') });
                    }
                    else {
                        setErrors({});
                        setUserAccount({ ...userAccount, password: userPassword });
                    }
                }
            },
            text:"Mot de passe (Minimum 8 caractères. Pas d'accent)"
        },
        {
            format: "checkbox",
            attributes : {
                id: "toggle-show-password",
                value: showPassword,
                onChange: () => setShowPassword(!showPassword),
            },
            text:"Afficher le mot de passe"
        },
        {
            format: "input",
            attributes : {
                id: "check-password",
                type: "password",
                title: "Confirmer le mot de passe",
                required: true,
                errorMessage: errors.checkPassword || null,
                onChange: (e) => {
                    let userPassword = e.target.value;
                    let checkPasswordError = checkPassword(userAccount.password, userPassword);
                    if(checkPasswordError) {
                        setErrors({ ...errors, checkPassword: checkPasswordError });
                    }
                    else {
                        setErrors({});
                    }
                }
            },
            text: "Confirmer le mot de passe (Doit être identique)"
        },
        {
            format: "submit",
            attributes: {
                type: "submit",
                title: "Créér mon compte",
            },
            text: "Créér mon compte"
        }
    ];
    

    // ================================ HANDLE API ================================ //
    async function signup(event) {
        /*
        
        */

        event.preventDefault();
        if(isUserInfoExist) {
            let jsonData = JSON.parse(isUserInfoExist);
            const response = await fetch(
                `${BACKEND_API_URL}/api/v1/register/account`,
                {
                    method: 'POST',
                    headers: { 'content-type': 'application/json' },
                    body: JSON.stringify({ ...userAccount, user_id: jsonData.user_id })
                }
            );

            if(response.ok) {
                const data = await response.json();
                if(data.success) {
                    localStorage.removeItem(LS_USER_INFO_KEY);
                    navigate("/login?c=true&redirection=true&from=account", { replace: true });
                }
            }
        }
    }
    

    // ================================ RENDER ================================ //
    return (
        <>
            <HeaderLayout />
            <BodyLayout>
                <CustomH2MediumTitle>
                    Créer un compte sur Task Manager
                </CustomH2MediumTitle>
                <FormLayout fields={accountFormStructures}
                            onSubmit={signup} />
            </BodyLayout>
            <FooterLayout />
        </>
    );
}


export default RegisterAccountPAge;