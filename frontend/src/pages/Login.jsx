import { useRef, useEffect, useState } from "react";

import { CustomBlueLink } from "../components/Ancres";
import { CustomBlueInput } from "../components/Inputs";
import { CustomBlueSubmitButton } from "../components/Buttons";
import { CustomH2MediumTitle, CustomErrorTitle } from "../components/Titles";



function LoginForm({ isUserNotAuth, isTooManyRequest, loginForms, references, onSubmit }) {
    /*

    */

    return (
        <form onSubmit={onSubmit} >
            {
                isUserNotAuth && <UserNotAuthentifiedError />
            }
            {
                isTooManyRequest && <TooManyRequestError />
            }
            {
                loginForms.map( (loginItem, index) => <CustomBlueInput
                            key={loginItem.id}
                            ref={references[index]}
                            id={loginItem.id}
                            type={loginItem.type}
                            placeholder={loginItem.placeholder}
                            title={loginItem.title}
                            required={loginItem.required} >
                        {loginItem.text}
                    </CustomBlueInput>
                )
            }
            <CustomBlueSubmitButton>
                Se connecter
            </CustomBlueSubmitButton>
        </form>
    );
}


function ForgotPassword() {
    /*
    
    */
    const textLink = "Mot de passe oublié ?";

    return (
        <div className="flex flex-row justify-center items-center my-[0.3em]" >
            <CustomBlueLink hrefLink="/forgot-password"
                            title={textLink} >
                {textLink}
            </CustomBlueLink>
        </div>
    );
}


function CreateNewAccount() {
    /*

    */

    const textLink = "Créér un nouveau compte";

    return (
        <div className="flex flex-row justify-center items-center my-[0.3em]" >
            <p>
                Vous n'avez pas encore de compte ?  
            </p>
            <CustomBlueLink hrefLink="/register" 
                            title={textLink} >
                {textLink}
            </CustomBlueLink>
        </div>
    );
}


function UserNotAuthentifiedError() {
    /*

    */
    return (
        <CustomErrorTitle >
            Identifiant ou mot de passe incorrecte
        </CustomErrorTitle>
    );
}


function TooManyRequestError() {
    /*

    */
    return (
        <CustomErrorTitle >
            Trop de requêtes sont en cours de traitements. Veuillez réessayer plus tard ou rafraîchir la page.
        </CustomErrorTitle>
    );
}


function LoginPage() {
    /*

    */

    // ================================ USES ================================ //
    const identityRef = useRef(null);
    const passwordRef = useRef(null);
    const [loginFormStructure, setLoginFormStructure] = useState(null);
    const [isUserNotAuth, setIsUserNotAuth] = useState(false);
    const [isTooManyRequest, setIsTooManyRequest] = useState(false);
    

    // ================================ HANDLE SUBMIT ================================ //
    async function sendLoginForm(event) {
        /*
        
        */

        event.preventDefault();

        const endPointUrl = 'http://localhost:8000/login/auth';
        
        try {
            const response = await fetch(
                endPointUrl,
                {
                    method:"POST",
                    body: JSON.stringify({
                        "identity": identityRef.current.value,
                        "password": passwordRef.current.value,
                        "timestamp": Math.floor(Date.now() / 1000)
                    }),
                    headers: { 'Content-Type': 'application/json' }
                }
            );
            // Error when sending request
            if(response.status == 429) {
                setIsTooManyRequest(true)
            }
            else if (response.status == 200) {
                const authData = await response.json();
                setIsUserNotAuth(!authData.authenticate)
            }
            else {
                throw new Error(`HTTP error: Failed to send request from "${endPointUrl}"`);
            }
        }
        catch (err) { console.error(err) }

    }


    // ================================ BUILD LOGIN INPUTS ================================ //
    useEffect( () => {

        async function builLoginForm() {
        
            const endPointUrl = 'http://localhost:8000/login/forms';
            try {
                const response = await fetch(endPointUrl);
                if(!response.ok) {
                    throw new Error(`HTTP error: Failed to send request from "${endPointUrl}"`);
                }
                setLoginFormStructure(await response.json());
            }
            catch (err) { console.error(err) }
        }

        builLoginForm();

    }, []);    

    // ================================ RENDER ================================ //
    return (
        <div className="flex flex-row justify-center" >
            <div className="flex flex-col text-center border border-1 border-[#086288] rounded-[1em] bg-white w-[50%] p-[3em] gap-y-[2em]" >
                <CustomH2MediumTitle>
                    Se connecter à Task Manager App
                    </CustomH2MediumTitle>
                {
                    loginFormStructure &&
                    <>
                        <LoginForm loginForms={loginFormStructure}
                                isUserNotAuth={isUserNotAuth}
                                isTooManyRequest={isTooManyRequest}
                                references={[identityRef, passwordRef]}
                                onSubmit={sendLoginForm} />
                    </>
                }
                <ForgotPassword />
                <CreateNewAccount />
            </div>
        </div>
    );
}


export default LoginPage; 