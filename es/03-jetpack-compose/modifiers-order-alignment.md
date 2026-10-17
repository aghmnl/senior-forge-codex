---
layout: page
title: "Modifiers: Order & Alignment"
lang: es
permalink: /es/03-jetpack-compose/modifiers-order-alignment/
order: 4
---

## The Theory (El Qué)

Un [`Modifier`]({{ "/es/glosario/modifier/" | relative_url }}) decora un composable: le puede dar tamaño, [padding]({{ "/es/glosario/padding/" | relative_url }}), dibujar detrás, recortarlo, hacerlo clickeable o posicionarlo. Los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) se encadenan, `Modifier.padding(8.dp).background(Color.Red)`, y **la cadena tiene orden**. Cada [modifier]({{ "/es/glosario/modifier/" | relative_url }}) envuelve todo lo que viene después, de afuera hacia adentro, así que cambiar el orden cambia el resultado:

- `Modifier.padding(16.dp).background(Color.Red)`: el [padding]({{ "/es/glosario/padding/" | relative_url }}) se aplica primero, afuera, así que funciona como un margen y el [fondo]({{ "/es/glosario/background/" | relative_url }}) rojo se dibuja solo adentro.
- `Modifier.background(Color.Red).padding(16.dp)`: el [fondo]({{ "/es/glosario/background/" | relative_url }}) cubre toda el área, y el [padding]({{ "/es/glosario/padding/" | relative_url }}) queda adentro, entre el borde rojo y el contenido.
- `Modifier.clickable { }.padding(16.dp)` hace que el [padding]({{ "/es/glosario/padding/" | relative_url }}) sea parte del [área táctil]({{ "/es/glosario/touch-target/" | relative_url }}); `Modifier.padding(16.dp).clickable { }` no.
- `Modifier.clip(CircleShape).background(...)` recorta lo que viene después, así que el [fondo]({{ "/es/glosario/background/" | relative_url }}) y el [ripple]({{ "/es/glosario/ripple/" | relative_url }}) de un [`clickable`]({{ "/es/glosario/clickable/" | relative_url }}) posterior quedan redondos; un [`clip`]({{ "/es/glosario/clip/" | relative_url }}) puesto después no los afecta.

**Los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) de tamaño siguen [constraints]({{ "/es/glosario/constraints/" | relative_url }}) (restricciones).** Un padre le pasa [constraints]({{ "/es/glosario/constraints/" | relative_url }}) a su hijo, y cada [modifier]({{ "/es/glosario/modifier/" | relative_url }}) de tamaño las acota para los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) que vienen después. En `Modifier.size(100.dp).size(50.dp)` el primero fija el tamaño en 100 dp y el segundo no lo puede cambiar: **gana el primer tamaño**. [`fillMaxWidth()`]({{ "/es/glosario/fill-max-width/" | relative_url }}) toma todo el ancho permitido, [`wrapContentSize()`]({{ "/es/glosario/wrap-content-size/" | relative_url }}) deja que el contenido sea más chico y lo posiciona, y [`requiredSize()`]({{ "/es/glosario/required-size/" | relative_url }}) ignora las [constraints]({{ "/es/glosario/constraints/" | relative_url }}) que recibe.

**La alineación la decide el layout padre**, y cada layout ofrece sus propias herramientas:

- **[`Row`]({{ "/es/glosario/row/" | relative_url }})** ubica a los hijos en horizontal. [`horizontalArrangement`]({{ "/es/glosario/arrangement/" | relative_url }}) los distribuye sobre el **[eje principal]({{ "/es/glosario/main-axis-cross-axis/" | relative_url }})** ([`Arrangement.Start`]({{ "/es/glosario/arrangement/" | relative_url }}), `SpaceBetween`, [`spacedBy(8.dp)`]({{ "/es/glosario/arrangement/" | relative_url }})), y [`verticalAlignment`]({{ "/es/glosario/alignment/" | relative_url }}) los posiciona sobre el **[eje transversal]({{ "/es/glosario/main-axis-cross-axis/" | relative_url }})** ([`Alignment.CenterVertically`]({{ "/es/glosario/alignment/" | relative_url }})).
- **[`Column`]({{ "/es/glosario/column/" | relative_url }})** es lo mismo rotado: [`verticalArrangement`]({{ "/es/glosario/arrangement/" | relative_url }}) en el [eje principal]({{ "/es/glosario/main-axis-cross-axis/" | relative_url }}), [`horizontalAlignment`]({{ "/es/glosario/alignment/" | relative_url }}) en el transversal.
- **[`Box`]({{ "/es/glosario/box/" | relative_url }})** apila a los hijos. [`contentAlignment`]({{ "/es/glosario/alignment/" | relative_url }}) posiciona a todos, y [`Modifier.align(Alignment.TopStart)`]({{ "/es/glosario/layout-scopes/" | relative_url }}) posiciona a uno.

[`Modifier.align`]({{ "/es/glosario/layout-scopes/" | relative_url }}) y [`Modifier.weight`]({{ "/es/glosario/weight/" | relative_url }}) solo existen adentro del scope del padre correcto ([`BoxScope`]({{ "/es/glosario/layout-scopes/" | relative_url }}), [`RowScope`]({{ "/es/glosario/layout-scopes/" | relative_url }}), [`ColumnScope`]({{ "/es/glosario/layout-scopes/" | relative_url }})), así que usarlos en el lugar equivocado no compila.

Por convención, un composable que emite UI recibe un parámetro **`modifier: Modifier = Modifier`**, el primero de los opcionales, y lo aplica a su elemento raíz.

## The Senior Perspective (El Porqué)

- **Leer la cadena como capas, de afuera hacia adentro.** El primer [modifier]({{ "/es/glosario/modifier/" | relative_url }}) es la capa más externa; cada uno de los siguientes trabaja adentro del espacio que dejaron los anteriores. Con ese modelo, "[padding]({{ "/es/glosario/padding/" | relative_url }}) antes del [fondo]({{ "/es/glosario/background/" | relative_url }}) es un margen" y "[clickable]({{ "/es/glosario/clickable/" | relative_url }}) antes del [padding]({{ "/es/glosario/padding/" | relative_url }}) agranda el [área táctil]({{ "/es/glosario/touch-target/" | relative_url }})" dejan de ser reglas para memorizar y se vuelven obvias. La mayoría de los bugs de layout en Compose son un bug de orden.
- **El orden decide qué puede tocar el usuario.** Un ícono chico con [`clickable`]({{ "/es/glosario/clickable/" | relative_url }}) aplicado después de `size(18.dp)` tiene un [área táctil]({{ "/es/glosario/touch-target/" | relative_url }}) de 18 dp, por debajo del mínimo de accesibilidad de 48 dp. Poner [`clickable`]({{ "/es/glosario/clickable/" | relative_url }}) antes del [padding]({{ "/es/glosario/padding/" | relative_url }}), o usar [`minimumInteractiveComponentSize()`]({{ "/es/glosario/touch-target/" | relative_url }}), lo hace alcanzable sin cambiar cómo se ve. Y [`clip`]({{ "/es/glosario/clip/" | relative_url }}) tiene que ir antes de [`clickable`]({{ "/es/glosario/clickable/" | relative_url }}) si el [ripple]({{ "/es/glosario/ripple/" | relative_url }}) debe seguir la forma.
- **Aplicar el [modifier]({{ "/es/glosario/modifier/" | relative_url }}) de quien llama primero, una vez, en la raíz.** Escribir `modifier.fillMaxWidth()` pone los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) de quien llama afuera de los del componente, así que un tamaño, un [padding]({{ "/es/glosario/padding/" | relative_url }}) o un [`align`]({{ "/es/glosario/layout-scopes/" | relative_url }}) de quien llama gana. Aplicar [`modifier`]({{ "/es/glosario/modifier/" | relative_url }}) a un hijo interno, aplicarlo dos veces, o encadenar un tamaño fijo propio antes, rompe lo que espera quien llama: su [padding]({{ "/es/glosario/padding/" | relative_url }}) termina en el lugar equivocado, o su tamaño se ignora.
- **El arrangement es del grupo, la alineación es de cada hijo.** [`spacedBy(8.dp)`]({{ "/es/glosario/arrangement/" | relative_url }}) es mejor que agregarle [padding]({{ "/es/glosario/padding/" | relative_url }}) a cada hijo, porque el espaciado le pertenece al padre, no a los ítems. [`weight(1f)`]({{ "/es/glosario/weight/" | relative_url }}) toma el espacio que queda después de medir a los hijos sin peso, que es la forma limpia de empujar un elemento al final de un [`Row`]({{ "/es/glosario/row/" | relative_url }}).
- **Los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) restringidos a un scope son una red de seguridad.** Como [`align`]({{ "/es/glosario/layout-scopes/" | relative_url }}) y [`weight`]({{ "/es/glosario/weight/" | relative_url }}) solo existen en sus scopes, el compilador impide pedirle a un padre un posicionamiento que no soporta. Cuando un [modifier]({{ "/es/glosario/modifier/" | relative_url }}) "no existe", la pregunta suele ser qué padre debería tomar esa decisión.
- **Algunos [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) tienen una forma diferida, con [lambda]({{ "/es/glosario/lambdas/" | relative_url }}), por rendimiento.** [`offset { }`]({{ "/es/glosario/modifier-offset/" | relative_url }}), [`graphicsLayer { }`]({{ "/es/glosario/graphics-layer/" | relative_url }}) y [`drawBehind { }`]({{ "/es/glosario/draw-behind/" | relative_url }}) leen el estado en la [fase de layout]({{ "/es/glosario/compose-phases/" | relative_url }}) o de dibujo en lugar de la [composition]({{ "/es/glosario/composition/" | relative_url }}), así que un valor que cambia en cada frame (scroll, arrastre, animación) no recompone el composable. Los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) que reciben valores comunes los leen durante la [composition]({{ "/es/glosario/composition/" | relative_url }}).

## Code in Action

```kotlin
// From FollowApp Suite — StateChip.kt
// The remove button of a chip: an 18 dp circle. clip comes before clickable, so
// the ripple of the click is clipped to the circle instead of a square.
Box(
    modifier = Modifier
        .size(18.dp)
        .clip(CircleShape)
        .clickable { onRemove() },
    contentAlignment = Alignment.Center
) {
    Icon(imageVector = Icons.Default.Close, contentDescription = removeContentDescription, /* ... */)
}

// From FollowApp Suite — CollapsibleGroupCard.kt
// A header chip straddling the top border of a card. The caller's modifier is
// applied first, at the root. The card surface is pushed down by half the chip
// height with padding, and the chip is aligned to the top start of the Box, so
// it sits half in, half out of the card.
Box(modifier = modifier.fillMaxWidth()) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = chipHalfHeight),
        shape = RoundedCornerShape(12.dp),
        color = containerColor,
    ) { /* content */ }

    Box(
        modifier = Modifier
            .align(Alignment.TopStart)
            .padding(start = 16.dp)
    ) {
        headerChip()
    }
}

// From FollowApp Suite — SelectionFloatingToolbar.kt
// Arrangement on the main axis (8 dp between buttons) and alignment on the cross
// axis (vertically centered), both decided by the Row, not by each button.
Surface(
    modifier = modifier,
    shape = RoundedCornerShape(28.dp),
    color = MaterialTheme.colorScheme.surfaceContainerHigh,
    shadowElevation = 6.dp
) {
    Row(
        modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        actions.forEach { action -> IconButton(onClick = action.onClick) { /* ... */ } }
    }
}

// Not found in FAS — standalone example
// Same modifiers, different order, different result.
Text("A", Modifier.padding(16.dp).background(Color.Red))   // margin, then red
Text("B", Modifier.background(Color.Red).padding(16.dp))   // red, with padding inside
Box(Modifier.size(100.dp).size(50.dp))                     // 100 dp: the first size wins
```

## The Interview (En el banquillo)

**Pregunta**: ¿Por qué importa el orden de los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) en Compose? Dame un ejemplo donde cambiarlo cambie el resultado.

**Respuesta Senior**: Porque una cadena de [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) no es un conjunto de propiedades, es una secuencia de envoltorios: cada [modifier]({{ "/es/glosario/modifier/" | relative_url }}) envuelve todo lo que viene después, de afuera hacia adentro. Así que el primer [modifier]({{ "/es/glosario/modifier/" | relative_url }}) es la capa más externa, y cada uno de los siguientes trabaja adentro del espacio que dejaron los anteriores. El ejemplo clásico es [padding]({{ "/es/glosario/padding/" | relative_url }}) y [fondo]({{ "/es/glosario/background/" | relative_url }}). `padding(16.dp).background(Red)` aplica el [padding]({{ "/es/glosario/padding/" | relative_url }}) afuera, así que se comporta como un margen y el área roja es más chica; `background(Red).padding(16.dp)` pinta toda el área de rojo y el [padding]({{ "/es/glosario/padding/" | relative_url }}) queda adentro. La misma lógica decide el [área táctil]({{ "/es/glosario/touch-target/" | relative_url }}): [`clickable`]({{ "/es/glosario/clickable/" | relative_url }}) antes de [`padding`]({{ "/es/glosario/padding/" | relative_url }}) hace tocable el [padding]({{ "/es/glosario/padding/" | relative_url }}), después no, algo que importa en íconos chicos y para el mínimo de 48 dp. Y [`clip`]({{ "/es/glosario/clip/" | relative_url }}) recorta solo lo que viene después, así que tiene que ir antes de [`background`]({{ "/es/glosario/background/" | relative_url }}) y [`clickable`]({{ "/es/glosario/clickable/" | relative_url }}) si la forma y el [ripple]({{ "/es/glosario/ripple/" | relative_url }}) tienen que ser redondos. Los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) de tamaño funcionan con [constraints]({{ "/es/glosario/constraints/" | relative_url }}) que bajan por la cadena, así que gana el primer tamaño: `size(100.dp).size(50.dp)` mide 100 dp. Cuando un layout se ve mal en Compose, lo primero que reviso es el orden de la cadena.

**Pregunta**: Estás construyendo un componente de tarjeta reutilizable. ¿Cómo manejás su parámetro [`modifier`]({{ "/es/glosario/modifier/" | relative_url }}), y cómo alineás su contenido?

**Respuesta Senior**: El componente recibe `modifier: Modifier = Modifier` como su primer parámetro opcional y lo aplica una vez, al elemento raíz, antes de sus propios [modifiers]({{ "/es/glosario/modifier/" | relative_url }}): `Box(modifier = modifier.fillMaxWidth())`. Eso pone los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) de quien llama afuera, así que un [padding]({{ "/es/glosario/padding/" | relative_url }}), un tamaño o un [`align`]({{ "/es/glosario/layout-scopes/" | relative_url }}) de quien llama se respetan. Si lo aplicara a un hijo interno, o pusiera un tamaño fijo propio antes, el [padding]({{ "/es/glosario/padding/" | relative_url }}) de quien llama terminaría en el lugar equivocado o su tamaño se ignoraría, y el componente se comportaría distinto de cualquier otro composable. Para el contenido, la alineación le pertenece al layout padre. En un [`Row`]({{ "/es/glosario/row/" | relative_url }}) uso [`horizontalArrangement`]({{ "/es/glosario/arrangement/" | relative_url }}), por ejemplo [`spacedBy`]({{ "/es/glosario/arrangement/" | relative_url }}), para distribuir a los hijos en el [eje principal]({{ "/es/glosario/main-axis-cross-axis/" | relative_url }}), y [`verticalAlignment`]({{ "/es/glosario/alignment/" | relative_url }}) para centrarlos en el [eje transversal]({{ "/es/glosario/main-axis-cross-axis/" | relative_url }}), en lugar de agregarle [padding]({{ "/es/glosario/padding/" | relative_url }}) a cada hijo. En un [`Box`]({{ "/es/glosario/box/" | relative_url }}) uso [`contentAlignment`]({{ "/es/glosario/alignment/" | relative_url }}) para todos los hijos o [`Modifier.align`]({{ "/es/glosario/layout-scopes/" | relative_url }}) para uno, y [`weight`]({{ "/es/glosario/weight/" | relative_url }}) en un [`Row`]({{ "/es/glosario/row/" | relative_url }}) o [`Column`]({{ "/es/glosario/column/" | relative_url }}) para darle el espacio restante a un elemento. Esos [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) de posicionamiento solo existen en el scope de su padre, así que el compilador me impide usarlos donde no tienen sentido.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
