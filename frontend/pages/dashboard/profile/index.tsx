import React, {useState} from "react";
import {signOut, useSession} from "next-auth/react";
import {Box, Button, Code, HStack, Spinner, Text, VStack} from "@chakra-ui/react";
import axios from "axios";
import Layout from "@/components/Layout";
import Link from "next/link";

export default function Home() {

  const {data: session, status} = useSession({required: true});

  if (status == "loading") {
    return <Spinner size="lg"/>;
  }

  if (session) {
    return (
    <Layout>
      <main className={"h-screen"}>{
        <>
        <div className="my-6 mx-auto max-w-xl">
          <h1 className="text-3xl font-extrabold text-center">Hello, {session.user?.email}</h1>
        </div>

        <div className={"flex items-center justify-center gap-2"}>
          <Link
            className="rounded-full w-full max-w-[150px] py-4 text-center justify-center items-center bg-blue-600 font-semibold text-lg text-white flex transition-all duration-500 hover:bg-blue-700"
            href={"/dashboard/profile/order"}
          >
            Order history
          </Link>
          <Link
            className="rounded-full w-full max-w-[150px] py-4 text-center justify-center items-center bg-blue-600 font-semibold text-lg text-white flex transition-all duration-500 hover:bg-blue-700"
            href={"/dashboard/profile/subscription"}
          >
            Subscription
          </Link>

        </div>
        </>
      }</main>
    </Layout>
    );
  }

  return <></>;
}