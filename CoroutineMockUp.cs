using System.Collections;
using UnityEngine;

public static class CoroutineMockUp
{
    public static IEnumerator EmptyCoroutine()
    {
        yield return null;
    }
}