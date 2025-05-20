const firebaseConfig =
{
    apiKey: "AIzaSyCg8nwAbDnI67GJHFjbubBJWODjkllBBl8",
    authDomain: "ministry-manager-a1978.firebaseapp.com",
    projectId: "ministry-manager-a1978",
    storageBucket: "ministry-manager-a1978.firebasestorage.app",
    messagingSenderId: "266475760973",
    appId: "1:266475760973:web:bba8122f119ead35d31b04"
};

firebaseConfig.initializeApp(firebaseConfig);
const db = firebaseConfig.firestore();
const auth = firebaseConfig.auth();